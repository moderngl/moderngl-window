"""
Wrapper for a loaded mesh / vao with properties
"""
from pyrr import matrix44


class Node:
    def __init__(self, camera=None, mesh=None, matrix=None):
        self.camera = camera
        self.mesh = mesh
        # Local matrix
        self.matrix = matrix
        # Global matrix
        self.matrix_global = None
        self.matrix_global_bytes = None

        self.children = []

    def add_child(self, child):
        """Add a child to this node"""
        self.children.append(child)

    def draw(self, projection_matrix=None, camera_matrix=None, time=0):
        """Draw node and children

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

        for child in self.children:
            child.draw(
                projection_matrix=projection_matrix,
                camera_matrix=camera_matrix,
                time=time
            )

    def draw_bbox(self, projection_matrix, camera_matrix, shader, vao):
        """Draw bounding box around the node"""
        if self.mesh:
            self.mesh.draw_bbox(
                projection_matrix,
                self.matrix_global_bytes,
                camera_matrix,
                shader,
                vao
            )

        for child in self.children:
            child.draw_bbox(projection_matrix, camera_matrix, shader, vao)

    def calc_global_bbox(self, view_matrix, bbox_min, bbox_max):
        """Recursive calculation of scene bbox"""
        if self.matrix is not None:
            view_matrix = matrix44.multiply(self.matrix, view_matrix)

        if self.mesh:
            bbox_min, bbox_max = self.mesh.calc_global_bbox(view_matrix, bbox_min, bbox_max)

        for child in self.children:
            bbox_min, bbox_max = child.calc_global_bbox(view_matrix, bbox_min, bbox_max)

        return bbox_min, bbox_max

    def calc_model_mat(self, model_matrix):
        """Calculate the model matrix related to all parents"""
        if self.matrix is not None:
            self.matrix_global = matrix44.multiply(self.matrix, model_matrix).astype('f4')
            self.matrix_global_bytes = self.matrix_global.tobytes()

            for child in self.children:
                child.calc_model_mat(self.matrix_global)
        else:
            self.matrix_global = model_matrix
            self.matrix_global_bytes = model_matrix.tobytes()

            for child in self.children:
                child.calc_model_mat(model_matrix)
