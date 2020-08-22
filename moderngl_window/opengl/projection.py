from typing import Tuple

import numpy as np
from pyrr import Matrix44


class Projection3D:
    """3D Projection"""

    def __init__(self, aspect_ratio=16 / 9, fov=75.0, near=1.0, far=100.0):
        """Create a 3D projection

        Keyword Args:
            aspect_ratio (float): Aspect ratio
            fov (float): Field of view
            near (float): Near plane value
            far (float): Far plane value
        """
        self._aspect_ratio = aspect_ratio
        self._fov = fov
        self._near = near
        self._far = far
        self._matrix = None
        self._matrix_bytes = None
        self.update()

    @property
    def aspect_ratio(self) -> float:
        """float: The projection's aspect ratio"""
        return self._aspect_ratio

    @property
    def fov(self) -> float:
        """float: Current field of view"""
        return self._fov

    @property
    def near(self) -> float:
        """float: Current near plane value"""
        return self._near

    @property
    def far(self) -> float:
        """float : Current far plane value"""
        return self._far

    @property
    def matrix(self) -> np.ndarray:
        """np.ndarray: Current numpy projection matrix"""
        return self._matrix

    def update(
        self,
        aspect_ratio: float = None,
        fov: float = None,
        near: float = None,
        far: float = None,
    ) -> None:
        """Update the projection matrix

        Keyword Args:
            aspect_ratio (float): Aspect ratio
            fov (float): Field of view
            near (float): Near plane value
            far (float): Far plane value
        """
        self._aspect_ratio = aspect_ratio or self._aspect_ratio
        self._fov = fov or self._fov
        self._near = near or self._near
        self._far = far or self._far

        self._matrix = Matrix44.perspective_projection(
            self._fov, self._aspect_ratio, self._near, self._far, dtype="f4",
        )
        self._matrix_bytes = self._matrix.tobytes()

    def tobytes(self) -> bytes:
        """Get the byte representation of the projection matrix

        Returns:
            bytes: byte representation of the projection matrix
        """
        return self._matrix_bytes

    @property
    def projection_constants(self) -> Tuple[float, float]:
        """
        (x, y) projection constants for the current projection.
        This is for example useful when reconstructing a view position
        of a fragment from a linearized depth value.
        """
        return (
            self._far / (self._far - self._near),
            (self._far * self._near) / (self._near - self._far),
        )
