from PIL.Image import Image
from typing import Any, Tuple


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
    def size(self) -> Tuple[int, int]:
        """Tuple[int, int]: Size of the image in pixels (width, height)"""
        raise NotImplementedError

    def get_pixel_data(self, components: int = 4):
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
        self.image = image

    @property
    def width(self) -> int:
        return self._image.size[0]

    @property
    def height(self) -> int:
        return self._image.size[1]

    @property
    def size(self) -> Tuple[int, int]:
        return self._image.size

    def get_pixel_data(self, components: int = 4):
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
