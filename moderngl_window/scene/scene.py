"""
Wrapper for a loaded scene with properties.
"""
from typing import TYPE_CHECKING
import logging
import numpy
from pyrr import matrix44, vector3

import moderngl
import moderngl_window as mglw
from moderngl_window.resources import programs
from moderngl_window.meta import ProgramDescription
from moderngl_window import geometry

from .programs import (
    ColorProgram,
    FallbackProgram,
    MeshProgram,
    TextureProgram,
)

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from moderngl_window.scene import Node, Material


class Scene:
    """Generic scene"""
    def __init__(self, name, **kwargs):
        """Create a scene with a name.

        Args:
            name (str): Unique name or path for the scene
        """
        self.name = name
        self.root_nodes = []

        # References resources in the scene
        self.nodes = []
        self.materials = []
        self.meshes = []
        self.cameras = []

        self.bbox_min = None  # Type: numpy.ndarray
        self.bbox_max = None  # Type: numpy.ndarray
        self.diagonal_size = 1.0

        self.bbox_vao = geometry.bbox()
        self.bbox_program = programs.load(
            ProgramDescription(path='scene_default/bbox.glsl'),
        )
        self._matrix = matrix44.create_identity(dtype='f4')

    @property
    def ctx(self) -> moderngl.Context:
        """moderngl.Context: The current context"""
        return mglw.ctx()

    @property
    def matrix(self) -> numpy.ndarray:
        """numpy.ndarray: The current model matrix

        This property is settable.
        """
        return self._matrix

    @matrix.setter
    def matrix(self, matrix: numpy.ndarray):
        self._matrix = matrix.astype('f4')
        for node in self.root_nodes:
            node.calc_model_mat(self._matrix)

    def draw(self, projection_matrix: numpy.ndarray = None, camera_matrix: numpy.ndarray = None, time=0.0) -> None:
        """Draw all the nodes in the scene.

        Args:
            projection_matrix (ndarray): projection matrix (bytes)
            camera_matrix (ndarray): camera_matrix (bytes)
            time (float): The current time
        """
        for node in self.root_nodes:
            node.draw(
                projection_matrix=projection_matrix.astype('f4'),
                camera_matrix=camera_matrix.astype('f4'),
                time=time,
            )

        self.ctx.clear_samplers(0, 4)

    def draw_bbox(self, projection_matrix=None, camera_matrix=None, children=True) -> None:
        """Draw scene and mesh bounding boxes.

        Args:
            projection_matrix (ndarray): mat4 projection
            camera_matrix (ndarray): mat4 camera matrix
            children (bool): Will draw bounding boxes for meshes as well
        """
        projection_matrix = projection_matrix.astype('f4')
        camera_matrix = camera_matrix.astype('f4')

        # Scene bounding box
        self.bbox_program["m_proj"].write(projection_matrix)
        self.bbox_program["m_model"].write(self._matrix)
        self.bbox_program["m_cam"].write(camera_matrix)
        self.bbox_program["bb_min"].write(self.bbox_min)
        self.bbox_program["bb_max"].write(self.bbox_max)
        self.bbox_program["color"].value = (1.0, 0.0, 0.0)
        self.bbox_vao.render(self.bbox_program)

        if not children:
            return

        # Draw bounding box for children
        for node in self.root_nodes:
            node.draw_bbox(projection_matrix, camera_matrix, self.bbox_program, self.bbox_vao)

    def apply_mesh_programs(self, mesh_programs=None) -> None:
        """Applies mesh programs to meshes.
        If not mesh programs are passed in we assign default ones.

        Args:
            mesh_programs (list): List of mesh programs to assign
        """
        if not mesh_programs:
            mesh_programs = [ColorProgram(), TextureProgram(), FallbackProgram()]

        for mesh in self.meshes:
            for mesh_prog in mesh_programs:
                instance = mesh_prog.apply(mesh)
                if instance is not None:
                    if isinstance(instance, MeshProgram):
                        mesh.mesh_program = mesh_prog
                        break
                    else:
                        raise ValueError("apply() must return a MeshProgram instance, not {}".format(type(instance)))

            if not mesh.mesh_program:
                logger.warning("WARING: No mesh program applied to '%s'", mesh.name)

    def calc_scene_bbox(self) -> None:
        """Calculate scene bbox"""
        bbox_min, bbox_max = None, None
        for node in self.root_nodes:
            bbox_min, bbox_max = node.calc_global_bbox(
                matrix44.create_identity(dtype='f4'),
                bbox_min,
                bbox_max
            )

        self.bbox_min = bbox_min
        self.bbox_max = bbox_max

        self.diagonal_size = vector3.length(self.bbox_max - self.bbox_min)

    def prepare(self) -> None:
        """prepare the scene for rendering.

        Calls ``apply_mesh_programs()`` assigning default meshprograms if needed
        and sets the model matrix.
        """
        self.apply_mesh_programs()
        # Recursively calculate model matrices
        self.matrix = matrix44.create_identity(dtype='f4')

    def find_node(self, name: str = None) -> 'Node':
        """Finds a :py:class:`~moderngl_window.scene.Node`

        Keyword Args:
            name (str): Case sensitive name
        Returns:
            A :py:class:`~moderngl_window.scene.Node` or ``None`` if not found.
        """
        for node in self.nodes:
            if node.name == name:
                return node

        return None

    def find_material(self, name: str = None) -> 'Material':
        """Finds a :py:class:`~moderngl_window.scene.Material`

        Keyword Args:
            name (str): Case sensitive material name
        Returns:
            A :py:class:`~moderngl_window.scene.Material` or ``None``
        """
        for mat in self.materials:
            if mat.name == name:
                return mat

        return None

    def destroy(self) -> None:
        """Destroys the scene data and vertex buffers"""
        for mesh in self.meshes:
            mesh.vao.release()

    def __str__(self) -> str:
        return "<Scene: {}>".format(self.name)

    def __repr__(self) -> str:
        return str(self)
