from typing import Tuple

from pyrr import Matrix44


class Projection:
    """"""
    def __init__(self, aspect_ratio=9 / 16, fov=75, near=1, far=100):
        """
        Keyword Args:
            aspect_ratio (float): Sspect ratio
            fov (float): Field of view
            near (float): Near plane value
            far (float): Far plane value
        """
        self.aspect_ratio = aspect_ratio
        self.fov = fov
        self.near = near
        self.far = far
        self.matrix = None
        self.update()

    def update(self, aspect_ratio=None, fov=None, near=None, far=None) -> None:
        """
        Update the internal projection matrix based on current values

        Keyword Args:
            aspect_ratio (float): Sspect ratio
            fov (float): Field of view
            near (float): Near plane value
            far (float): Far plane value
        """
        self.aspect_ratio = aspect_ratio or self.aspect_ratio
        self.fov = fov or self.fov
        self.near = near or self.near
        self.far = far or self.far

        self.matrix = Matrix44.perspective_projection(self.fov, self.aspect_ratio, self.near, self.far)

    def tobytes(self) -> bytes:
        return self.matrix.astype('f4').tobytes()

    @property
    def projection_constants(self) -> Tuple[float, float]:
        """
        (x, y) projection constants for the current projection.
        This is for example useful when reconstructing a view position
        of a fragment from a linearized depth value.
        """
        return self.far / (self.far - self.near), (self.far * self.near) / (self.near - self.far)
