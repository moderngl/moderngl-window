"""
Wrapper for a loaded scene with properties.
"""
import numpy
from pyrr import matrix44, vector3

import moderngl
import moderngl_window as mglw
from moderngl_window.resources import programs
from moderngl_window.resources.meta import ProgramDescription

from .programs import (
    ColorProgram,
    FallbackProgram,
    MeshProgram,
    TextureProgram,
)


class Scene:
    """Generic scene"""
    def __init__(self, name, **kwargs):
        """
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

        # self.bbox_vao = geometry.bbox()
        self.bbox_program = programs.load(ProgramDescription(
            label='scene_default/bbox.glsl',
            path='scene_default/bbox.glsl'),
        )
        self._view_matrix = matrix44.create_identity()

    @property
    def ctx(self) -> moderngl.Context:
        """moderngl.Context: The current context"""
        return mglw.ctx()

    @property
    def view_matrix(self) -> numpy.ndarray:
        """numpy.ndarray: The current view matrix

        This property is settable.
        """
        return self._view_matrix

    @view_matrix.setter
    def view_matrix(self, matrix: numpy.ndarray):
        self._view_matrix = matrix.astype('f4')
        for node in self.root_nodes:
            node.calc_view_mat(self._view_matrix)

    def draw(self, projection_matrix: numpy.ndarray = None, camera_matrix: numpy.ndarray = None, time=0.0):
        """
        Draw all the nodes in the scene

        Args:
            projection_matrix (ndarray): projection matrix (bytes)
            camera_matrix (ndarray): camera_matrix (bytes)
            time (float): The current time
        """
        projection_matrix = projection_matrix.astype('f4').tobytes()
        camera_matrix = camera_matrix.astype('f4').tobytes()

        for node in self.root_nodes:
            node.draw(
                projection_matrix=projection_matrix,
                camera_matrix=camera_matrix,
                time=time,
            )

        self.ctx.clear_samplers(0, 4)

    def draw_bbox(self, projection_matrix=None, camera_matrix=None, children=True) -> None:
        """Draw scene and mesh bounding boxes
        
        Args:
            projection_matrix (ndarray): mat4 projection
            camera_matrix (ndarray): mat4 camera matrix
            children (bool): Will draw bounding boxes for meshes as well
        """
        projection_matrix = projection_matrix.astype('f4').tobytes()
        camera_matrix = camera_matrix.astype('f4').tobytes()

        # Scene bounding box
        self.bbox_program["m_proj"].write(projection_matrix)
        self.bbox_program["m_view"].write(self._view_matrix.astype('f4').tobytes())
        self.bbox_program["m_cam"].write(camera_matrix)
        self.bbox_program["bb_min"].write(self.bbox_min.astype('f4').tobytes())
        self.bbox_program["bb_max"].write(self.bbox_max.astype('f4').tobytes())
        self.bbox_program["color"].value = (1.0, 0.0, 0.0)
        self.bbox_vao.render(self.bbox_program)

        if not children:
            return

        # Draw bounding box for children
        for node in self.root_nodes:
            node.draw_bbox(projection_matrix, camera_matrix, self.bbox_program, self.bbox_vao)

    def apply_mesh_programs(self, mesh_programs=None) -> None:
        """Applies mesh programs to meshes
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
                print("WARING: No mesh program applied to '{}'".format(mesh.name))

    def calc_scene_bbox(self) -> None:
        """Calculate scene bbox"""
        bbox_min, bbox_max = None, None
        for node in self.root_nodes:
            bbox_min, bbox_max = node.calc_global_bbox(
                matrix44.create_identity(),
                bbox_min,
                bbox_max
            )

        self.bbox_min = bbox_min
        self.bbox_max = bbox_max

        self.diagonal_size = vector3.length(self.bbox_max - self.bbox_min)

    def prepare(self) -> None:
        """prepare the scene for rendering.
        This is mostly to ensure shaders are assigned.
        """
        self.apply_mesh_programs()
        self.view_matrix = matrix44.create_identity()

    def destroy(self) -> None:
        """Destroys the scene data and vertex buffers"""
        for mesh in self.meshes:
            mesh.vao.release()

    def __str__(self):
        return "<Scene: {}>".format(self.name)

    def __repr__(self):
        return str(self)
