"""
Wrapper for a loaded scene with properties.
"""

import logging
from typing import TYPE_CHECKING, Any, Optional

import glm
import moderngl

import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window.meta import ProgramDescription
from moderngl_window.resources.programs import programs

from .material import Material
from .node import Node
from .programs import (
    ColorLightProgram,
    FallbackProgram,
    MeshProgram,
    TextureLightProgram,
    TextureProgram,
    TextureVertexColorProgram,
    VertexColorProgram,
)

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from moderngl_window.scene import Camera, Material, Mesh, Node


class Scene:
    """Generic scene"""

    def __init__(self, name: Optional[str], **kwargs: Any):
        """Create a scene with a name.

        Args:
            name (str): Unique name or path for the scene
        """
        self.name = name
        self.root_nodes: list[Node] = []

        # References resources in the scene
        self.nodes: list[Node] = []
        self.materials: list[Material] = []
        self.meshes: list[Mesh] = []
        self.cameras: list[Camera] = []

        self.bbox_min: glm.vec3 = glm.vec3()
        self.bbox_max: glm.vec3 = glm.vec3()
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
    def matrix(self) -> glm.mat4:
        """glm.mat4x4: The current model matrix

        This property is settable.
        """
        return self._matrix

    @matrix.setter
    def matrix(self, matrix: glm.mat4) -> None:
        self._matrix = matrix
        for node in self.root_nodes:
            node.calc_model_mat(self._matrix)

    def draw(
        self,
        projection_matrix: Optional[glm.mat4] = None,
        camera_matrix: Optional[glm.mat4] = None,
        time: float = 0.0,
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
        projection_matrix: Optional[glm.mat4] = None,
        camera_matrix: Optional[glm.mat4] = None,
        children: float = True,
        color: tuple[float, float, float] = (0.75, 0.75, 0.75),
    ) -> None:
        """Draw scene and mesh bounding boxes.

        Args:
            projection_matrix (glm.mat4): mat4 projection
            camera_matrix (glm.mat4): mat4 camera matrix
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
        self,
        projection_matrix: Optional[glm.mat4] = None,
        camera_matrix: Optional[glm.mat4] = None,
        color: tuple[float, float, float, float] = (0.75, 0.75, 0.75, 1.0),
    ) -> None:
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

    def apply_mesh_programs(
        self, mesh_programs: Optional[list[MeshProgram]] = None, clear: bool = True
    ) -> None:
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
        bbox_min: Optional[glm.vec3] = None
        bbox_max: Optional[glm.vec3] = None
        for node in self.root_nodes:
            bbox_min, bbox_max = node.calc_global_bbox(glm.mat4(), bbox_min, bbox_max)

        assert (bbox_max is not None) and (
            bbox_min is not None
        ), "The bounding are not defined, please make sure your code is correct"

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

    def find_node(self, name: Optional[str] = None) -> Optional[Node]:
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

    def find_material(self, name: Optional[str] = None) -> Optional[Material]:
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

    def release(self) -> None:
        """Destroys the scene data and vertex buffers"""
        self.destroy()

    def destroy(self) -> None:
        """Destroys the scene data and vertex buffers"""
        for mesh in self.meshes:
            if mesh.vao is not None:
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
