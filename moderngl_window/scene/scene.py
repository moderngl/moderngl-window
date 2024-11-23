"""
Wrapper for a loaded scene with properties.
"""

from typing import TYPE_CHECKING
import logging
import numpy
import glm

import moderngl
import moderngl_window as mglw
from moderngl_window.resources import programs
from moderngl_window.meta import ProgramDescription
from moderngl_window import geometry

from .programs import (
    FallbackProgram,
    VertexColorProgram,
    ColorLightProgram,
    MeshProgram,
    TextureProgram,
    TextureVertexColorProgram,
    TextureLightProgram,
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

        if self.ctx.extra is None:
            self.ctx.extra = {}

        # Load bbox program and cache in the context
        self.bbox_program = self.ctx.extra.get("DEFAULT_BBOX_PROGRAM")
        if not self.bbox_program:
            self.bbox_program = programs.load(
                ProgramDescription(path="scene_default/bbox.glsl"),
            )
            self.ctx.extra["DEFAULT_BBOX_PROGRAM"] = self.bbox_program

        # Load wireframe program and cache in the context
        self.wireframe_program = self.ctx.extra.get("DEFAULT_WIREFRAME_PROGRAM")
        if not self.wireframe_program:
            self.wireframe_program = programs.load(
                ProgramDescription(path="scene_default/wireframe.glsl"),
            )
            self.ctx.extra["DEFAULT_WIREFRAME_PROGRAM"] = self.wireframe_program

        self._matrix = glm.mat4()

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
    def matrix(self, matrix: glm.mat4):
        self._matrix = matrix
        for node in self.root_nodes:
            node.calc_model_mat(self._matrix)

    def draw(
        self,
        projection_matrix: glm.mat4 = None,
        camera_matrix: glm.mat4 = None,
        time=0.0,
    ) -> None:
        """Draw all the nodes in the scene.

        Args:
            projection_matrix (ndarray): projection matrix (bytes)
            camera_matrix (ndarray): camera_matrix (bytes)
            time (float): The current time
        """
        for node in self.root_nodes:
            node.draw(
                projection_matrix=projection_matrix,
                camera_matrix=camera_matrix,
                time=time,
            )

        self.ctx.clear_samplers(0, 4)

    def draw_bbox(
        self,
        projection_matrix=None,
        camera_matrix=None,
        children=True,
        color=(0.75, 0.75, 0.75),
    ) -> None:
        """Draw scene and mesh bounding boxes.

        Args:
            projection_matrix (ndarray): mat4 projection
            camera_matrix (ndarray): mat4 camera matrix
            children (bool): Will draw bounding boxes for meshes as well
            color (tuple): Color of the bounding boxes
        """
        projection_matrix = projection_matrix
        camera_matrix = camera_matrix

        # Scene bounding box
        self.bbox_program["m_proj"].write(projection_matrix)
        self.bbox_program["m_model"].write(self._matrix)
        self.bbox_program["m_cam"].write(camera_matrix)
        self.bbox_program["bb_min"].write(self.bbox_min)
        self.bbox_program["bb_max"].write(self.bbox_max)
        self.bbox_program["color"].value = color
        self.bbox_vao.render(self.bbox_program)

        if not children:
            return

        # Draw bounding box for children
        for node in self.root_nodes:
            node.draw_bbox(projection_matrix, camera_matrix, self.bbox_program, self.bbox_vao)

    def draw_wireframe(
        self, projection_matrix=None, camera_matrix=None, color=(0.75, 0.75, 0.75, 1.0)
    ):
        """Render the scene in wireframe mode.

        Args:
            projection_matrix (ndarray): mat4 projection
            camera_matrix (ndarray): mat4 camera matrix
            children (bool): Will draw bounding boxes for meshes as well
            color (tuple): Color of the wireframes
        """
        projection_matrix = projection_matrix
        camera_matrix = camera_matrix

        self.wireframe_program["m_proj"].write(projection_matrix)
        self.wireframe_program["m_model"].write(self._matrix)
        self.wireframe_program["m_cam"].write(camera_matrix)
        self.wireframe_program["color"] = color

        # Draw bounding box for children
        self.ctx.wireframe = True

        for node in self.root_nodes:
            node.draw_wireframe(projection_matrix, camera_matrix, self.wireframe_program)

        self.ctx.wireframe = False

    def apply_mesh_programs(self, mesh_programs=None, clear: bool = True) -> None:
        """Applies mesh programs to meshes.
        If not mesh programs are passed in we assign default ones.

        Args:
            mesh_programs (list): List of mesh programs to assign
            clear (bool): Clear all assigned mesh programs
        """
        global DEFAULT_PROGRAMS

        if clear:
            for mesh in self.meshes:
                mesh.mesh_program = None

        if not mesh_programs:
            mesh_programs = self.ctx.extra.get("DEFAULT_PROGRAMS")
            if not mesh_programs:
                mesh_programs = [
                    TextureLightProgram(),
                    TextureProgram(),
                    VertexColorProgram(),
                    TextureVertexColorProgram(),
                    ColorLightProgram(),
                    FallbackProgram(),
                ]
                self.ctx.extra["DEFAULT_PROGRAMS"] = mesh_programs

        for mesh in self.meshes:
            for mesh_prog in mesh_programs:
                instance = mesh_prog.apply(mesh)
                if instance is not None:
                    if isinstance(instance, MeshProgram):
                        mesh.mesh_program = mesh_prog
                        break
                    else:
                        raise ValueError(
                            "apply() must return a MeshProgram instance, not {}".format(
                                type(instance)
                            )
                        )

            if not mesh.mesh_program:
                logger.warning("WARING: No mesh program applied to '%s'", mesh.name)

    def calc_scene_bbox(self) -> None:
        """Calculate scene bbox"""
        bbox_min, bbox_max = None, None
        for node in self.root_nodes:
            bbox_min, bbox_max = node.calc_global_bbox(glm.mat4(), bbox_min, bbox_max)

        self.bbox_min = bbox_min
        self.bbox_max = bbox_max

        self.diagonal_size = glm.length(self.bbox_max - self.bbox_min)

    def prepare(self) -> None:
        """prepare the scene for rendering.

        Calls ``apply_mesh_programs()`` assigning default meshprograms if needed
        and sets the model matrix.
        """
        self.apply_mesh_programs()
        # Recursively calculate model matrices
        self.matrix = glm.mat4()

    def find_node(self, name: str = None) -> "Node":
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

    def find_material(self, name: str = None) -> "Material":
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

    def release(self):
        """Destroys the scene data and vertex buffers"""
        self.destroy()

    def destroy(self) -> None:
        """Destroys the scene data and vertex buffers"""
        for mesh in self.meshes:
            mesh.vao.release()
            # if mesh.mesh_program:
            #     mesh.mesh_program.program.release()

        for mat in self.materials:
            mat.release()

        self.meshes = []
        self.root_nodes = []

    def __str__(self) -> str:
        return "<Scene: {}>".format(self.name)

    def __repr__(self) -> str:
        return str(self)
