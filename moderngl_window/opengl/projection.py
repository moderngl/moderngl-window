from typing import Optional

import glm


class Projection3D:
    """3D Projection"""

    def __init__(
        self, aspect_ratio: float = 16 / 9, fov: float = 75.0, near: float = 1.0, far: float = 100.0
    ):
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
        self._matrix = glm.mat4(0)
        self._matrix_bytes = bytes(0)
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
    def matrix(self) -> glm.mat4:
        """glm.mat4x4: Current projection matrix"""
        return self._matrix

    def update(
        self,
        aspect_ratio: Optional[float] = None,
        fov: Optional[float] = None,
        near: Optional[float] = None,
        far: Optional[float] = None,
    ) -> None:
        """Update the projection matrix

        Keyword Args:
            aspect_ratio (float): Aspect ratio
            fov (float): Field of view
            near (float): Near plane value
            far (float): Far plane value
        """
        if aspect_ratio is not None:
            self._aspect_ratio = aspect_ratio
        if fov is not None:
            self._fov = fov
        if near is not None:
            self._near = near
        if far is not None:
            self._far = far

        self._matrix = glm.perspective(
            glm.radians(self._fov), self._aspect_ratio, self._near, self._far
        )
        self._matrix_bytes = self._matrix.to_bytes()

    def tobytes(self) -> bytes:
        """Get the byte representation of the projection matrix

        Returns:
            bytes: byte representation of the projection matrix
        """
        return self._matrix_bytes

    @property
    def projection_constants(self) -> tuple[float, float]:
        """
        (x, y) projection constants for the current projection.
        This is for example useful when reconstructing a view position
        of a fragment from a linearized depth value.
        """
        return (
            self._far / (self._far - self._near),
            (self._far * self._near) / (self._near - self._far),
        )
