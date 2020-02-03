"""
Wrapper for a loaded mesh / vao with properties
"""
from pyrr import matrix44


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
        self.camera = camera
        self.mesh = mesh
        # Local matrix
        self.matrix = matrix
        # Global matrix
        self.matrix_global = None
        self.matrix_global_bytes = None

        self._children = []

    @property
    def name(self) -> str:
        """str: Get or set the node name"""
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def children(self):
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
        if self.mesh:
            self.mesh.draw(
                projection_matrix=projection_matrix,
                model_matrix=self.matrix_global_bytes,
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
        if self.mesh:
            self.mesh.draw_bbox(
                projection_matrix,
                self.matrix_global_bytes,
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
        if self.matrix is not None:
            view_matrix = matrix44.multiply(self.matrix, view_matrix)

        if self.mesh:
            bbox_min, bbox_max = self.mesh.calc_global_bbox(view_matrix, bbox_min, bbox_max)

        for child in self._children:
            bbox_min, bbox_max = child.calc_global_bbox(view_matrix, bbox_min, bbox_max)

        return bbox_min, bbox_max

    def calc_model_mat(self, model_matrix):
        """Calculate the model matrix related to all parents.

        Args:
            model_matrix (numpy.ndarray): model matrix
        """
        if self.matrix is not None:
            self.matrix_global = matrix44.multiply(self.matrix, model_matrix).astype('f4')
            self.matrix_global_bytes = self.matrix_global.tobytes()

            for child in self._children:
                child.calc_model_mat(self.matrix_global)
        else:
            self.matrix_global = model_matrix
            self.matrix_global_bytes = model_matrix.tobytes()

            for child in self._children:
                child.calc_model_mat(model_matrix)

    def __repr__(self):
        return "<Node name={}>".format(self.name)
