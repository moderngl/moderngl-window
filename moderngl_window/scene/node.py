"""
Wrapper for a loaded mesh / vao with properties
"""

from typing import Optional

import glm
import moderngl

from moderngl_window.opengl.vao import VAO

from .camera import Camera
from .mesh import Mesh


class Node:
    """A generic scene node containing a mesh or camera
    and/or a container for other nodes. Nodes and their children
    represents the scene tree.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        camera: Optional[Camera] = None,
        mesh: Optional[Mesh] = None,
        matrix: Optional[glm.mat4] = None,
    ):
        """Create a node.

        Keyword Args:
            name: Name of the node
            camera: Camera to store in the node
            mesh: Mesh to store in the node
            matrix: The node's matrix
        """
        self._name = name
        self._camera = camera
        self._mesh = mesh
        # Local node matrix
        self._matrix = matrix
        # Global matrix
        self._matrix_global = glm.mat4(1.0)

        self._children: list["Node"] = []

    @property
    def name(self) -> Optional[str]:
        """str: Get or set the node name"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def mesh(self) -> Optional[Mesh]:
        """:py:class:`~moderngl_window.scene.Mesh`: The mesh if present"""
        return self._mesh

    @mesh.setter
    def mesh(self, value: Mesh) -> None:
        self._mesh = value

    @property
    def camera(self) -> Optional[Camera]:
        """:py:class:`~moderngl_window.scene.Camera`: The camera if present"""
        return self._camera

    @camera.setter
    def camera(self, value: Camera) -> None:
        self._camera = value

    @property
    def matrix(self) -> Optional[glm.mat4]:
        """glm.mat4x4: Note matrix (local)"""
        return self._matrix

    @matrix.setter
    def matrix(self, value: glm.mat4) -> None:
        self._matrix = value

    @property
    def matrix_global(self) -> Optional[glm.mat4]:
        """glm.matx4: The global node matrix containing transformations from parent nodes"""
        return self._matrix_global

    @matrix_global.setter
    def matrix_global(self, value: glm.mat4) -> None:
        self._matrix_global = value

    @property
    def children(self) -> list["Node"]:
        """list: List of children"""
        return self._children

    def add_child(self, node: "Node") -> None:
        """Add a child to this node

        Args:
            node (Node): Node to add as a child
        """
        self._children.append(node)

    def draw(
        self,
        projection_matrix: glm.mat4,
        camera_matrix: glm.mat4,
        time: float = 0.0,
    ) -> None:
        """Draw node and children.

        Keyword Args:
            projection_matrix: projection matrix
            camera_matrix: camera_matrix
            time: The current time
        """
        if self._mesh:
            self._mesh.draw(
                projection_matrix=projection_matrix,
                model_matrix=self._matrix_global,
                camera_matrix=camera_matrix,
                time=time,
            )

        for child in self._children:
            child.draw(
                projection_matrix=projection_matrix,
                camera_matrix=camera_matrix,
                time=time,
            )

    def draw_bbox(
        self,
        projection_matrix: Optional[glm.mat4],
        camera_matrix: Optional[glm.mat4],
        program: moderngl.Program,
        vao: VAO,
    ) -> None:
        """Draw bounding box around the node and children.

        Keyword Args:
            projection_matrix: projection matrix
            camera_matrix: camera_matrix
            program (moderngl.Program): The program to render the bbox
            vao: The vertex array representing the bounding box
        """
        if self._mesh:
            assert (
                projection_matrix is not None
            ), "Can not draw bbox, the projection matrix is empty"
            assert self._matrix_global is not None, "Can not draw bbox, the global matrix is empty"
            assert camera_matrix is not None, "Can not draw bbox, the camera matrix is empty"
            self._mesh.draw_bbox(
                projection_matrix, self._matrix_global, camera_matrix, program, vao
            )

        for child in self.children:
            child.draw_bbox(projection_matrix, camera_matrix, program, vao)

    def draw_wireframe(
        self,
        projection_matrix: Optional[glm.mat4],
        camera_matrix: Optional[glm.mat4],
        program: moderngl.Program,
    ) -> None:
        """Render the node as wireframe.

        Keyword Args:
            projection_matrix (bytes): projection matrix
            camera_matrix (bytes): camera_matrix
            program (moderngl.Program): The program to render wireframe
        """
        if self._mesh:
            assert (
                projection_matrix is not None
            ), "Can not draw bbox, the projection matrix is empty"
            assert self._matrix_global is not None, "Can not draw bbox, the global matrix is empty"
            self._mesh.draw_wireframe(projection_matrix, self._matrix_global, program)

        for child in self.children:
            child.draw_wireframe(projection_matrix, self._matrix_global, program)

    def calc_global_bbox(
        self, view_matrix: glm.mat4, bbox_min: glm.vec3 | None, bbox_max: glm.vec3 | None
    ) -> tuple[glm.vec3, glm.vec3]:
        """Recursive calculation of scene bbox.

        Keyword Args:
            view_matrix (numpy.ndarray): view matrix
            bbox_min: min bbox values
            bbox_max: max bbox values
        """
        if self._matrix is not None:
            view_matrix = self._matrix * view_matrix

        if self._mesh:
            bbox_min, bbox_max = self._mesh.calc_global_bbox(view_matrix, bbox_min, bbox_max)

        for child in self._children:
            bbox_min, bbox_max = child.calc_global_bbox(view_matrix, bbox_min, bbox_max)

        return bbox_min, bbox_max

    def calc_model_mat(self, parent_matrix: glm.mat4) -> None:
        """Calculate the model matrix related to all parents.

        Args:
            parent_matrix: Matrix for parent node
        """
        if self._matrix is not None:
            self._matrix_global = parent_matrix * self._matrix

            for child in self._children:
                child.calc_model_mat(self._matrix_global)
        else:
            self._matrix_global = parent_matrix

            for child in self._children:
                child.calc_model_mat(parent_matrix)

    def __repr__(self) -> str:
        return "<Node name={}>".format(self.name)
