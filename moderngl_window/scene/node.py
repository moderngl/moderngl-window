"""
Wrapper for a loaded mesh / vao with properties
"""
from typing import List, TYPE_CHECKING
import numpy
from pyrr import matrix44

if TYPE_CHECKING:
    from moderngl_window.scene import Camera, Mesh


class Node:
    """A generic scene node containing a mesh or camera
    and/or a container for other nodes. Nodes and their children
    represents the scene tree.
    """
    def __init__(self, name=None, camera=None, mesh=None, matrix=None):
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
        self._matrix = matrix.astype('f4') if matrix is not None else None
        # Global matrix
        self._matrix_global = None

        self._children = []

    @property
    def name(self) -> str:
        """str: Get or set the node name"""
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def mesh(self) -> 'Mesh':
        """:py:class:`~moderngl_window.scene.Mesh`: The mesh if present"""
        return self._mesh

    @mesh.setter
    def mesh(self, value: 'Mesh'):
        self._mesh = value

    @property
    def camera(self) -> 'Camera':
        """:py:class:`~moderngl_window.scene.Camera`: The camera if present"""
        return self._camera

    @camera.setter
    def camera(self, value):
        self._camera = value

    @property
    def matrix(self) -> numpy.ndarray:
        """numpy.ndarray: Note matrix (local)"""
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        self._matrix = value

    @property
    def matrix_global(self) -> numpy.ndarray:
        """numpy.ndarray: The global node matrix containing transformations from parent nodes"""
        return self._matrix_global

    @matrix_global.setter
    def matrix_global(self, value):
        self._matrix_global = value

    @property
    def children(self) -> List['Node']:
        """list: List of children"""
        return self._children

    def add_child(self, node):
        """Add a child to this node

        Args:
            node (Node): Node to add as a child
        """
        self._children.append(node)

    def draw(self, projection_matrix=None, camera_matrix=None, time=0):
        """Draw node and children.

        Keyword Args:
            projection_matrix (bytes): projection matrix
            camera_matrix (bytes): camera_matrix
            time (float): The current time
        """
        if self._mesh:
            self._mesh.draw(
                projection_matrix=projection_matrix,
                model_matrix=self._matrix_global,
                camera_matrix=camera_matrix,
                time=time
            )

        for child in self._children:
            child.draw(
                projection_matrix=projection_matrix,
                camera_matrix=camera_matrix,
                time=time
            )

    def draw_bbox(self, projection_matrix, camera_matrix, program, vao):
        """Draw bounding box around the node and children.

        Keyword Args:
            projection_matrix (bytes): projection matrix
            camera_matrix (bytes): camera_matrix
            program (moderngl.Program): The program to render the bbox
            vao: The vertex array representing the bounding box
        """
        if self._mesh:
            self._mesh.draw_bbox(
                projection_matrix,
                self._matrix_global,
                camera_matrix,
                program,
                vao
            )

        for child in self.children:
            child.draw_bbox(projection_matrix, camera_matrix, program, vao)

    def calc_global_bbox(self, view_matrix, bbox_min, bbox_max):
        """Recursive calculation of scene bbox.

        Keyword Args:
            view_matrix (numpy.ndarray): view matrix
            bbox_min: min bbox values
            bbox_max: max bbox values
        """
        if self._matrix is not None:
            view_matrix = matrix44.multiply(self._matrix, view_matrix)

        if self._mesh:
            bbox_min, bbox_max = self._mesh.calc_global_bbox(view_matrix, bbox_min, bbox_max)

        for child in self._children:
            bbox_min, bbox_max = child.calc_global_bbox(view_matrix, bbox_min, bbox_max)

        return bbox_min, bbox_max

    def calc_model_mat(self, model_matrix):
        """Calculate the model matrix related to all parents.

        Args:
            model_matrix (numpy.ndarray): model matrix
        """
        if self._matrix is not None:
            self._matrix_global = matrix44.multiply(self._matrix, model_matrix).astype('f4')

            for child in self._children:
                child.calc_model_mat(self._matrix_global)
        else:
            self._matrix_global = model_matrix.astype('f4')

            for child in self._children:
                child.calc_model_mat(model_matrix)

    def __repr__(self):
        return "<Node name={}>".format(self.name)
