from typing import Any

from PIL.Image import Image


class BaseImage:
    """
    Base class for atlas images.
    Must be hashable for use as dict keys and in sets
    and decides the uniqueness of the image.
    """

    def __init__(self, image: Any):
        self._image = image

    @property
    def width(self) -> int:
        """int: Width of the image in pixels"""
        raise NotImplementedError

    @property
    def height(self) -> int:
        """int: Height of the image in pixels"""
        raise NotImplementedError

    @property
    def size(self) -> tuple[int, int]:
        """tuple[int, int]: Size of the image in pixels (width, height)"""
        raise NotImplementedError

    def get_pixel_data(self, components: int = 4) -> bytes:
        """
        Get the raw pixel data from the image.

        Keyword Args:
            components: Number of components to get
        """
        raise NotImplementedError

    def __hash__(self) -> int:
        return id(self)


class AtlasImage(BaseImage):
    """An atlas image using Pillow"""

    def __init__(self, image: Image):
        self._image = image

    @property
    def width(self) -> int:
        return self._image.width

    @property
    def height(self) -> int:
        return self._image.height

    @property
    def size(self) -> tuple[int, int]:
        return self._image.size

    def get_pixel_data(self, components: int = 4) -> bytes:
        """
        Get the raw pixel data from the image.

        Keyword Args:
            components: Number of components to get
        """
        if components == 4:
            return self._image.convert("RGBA").tobytes()
        elif components == 3:
            return self._image.covert("RGB").tobytes()
        else:
            raise ValueError("Only supports 3 or 4 components")
