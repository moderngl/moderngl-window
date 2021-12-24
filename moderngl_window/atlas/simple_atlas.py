from typing import Tuple

import moderngl
from .base import BaseImage


class SimpleAtlas:
    """
    A simple RGBA texture atlas using a row based allocation.
    There are more efficient ways to pack textures, but this
    is normally sufficient for dynamic atlases were textures
    are added on the fly runtime.
    """
    def __init__(self, ctx: moderngl.Context, width: int, height: int, border: int = 1):
        # Basic properties
        self._ctx = ctx
        self._width = width
        self._height = height
        # Atlas content
        self._texture = self._ctx.texture(self.size, components=4)
        # We want to be able to render into the atlas texture
        self._fbo = self._fbo = self._ctx.framebuffer(
            color_attachments=[self._texture]
        )

    @property
    def ctx(self) -> moderngl.Context:
        """The moderngl contex this atlas belongs to"""
        return self._ctx

    @property
    def textrue(self) -> moderngl.Texture:
        """The moderngl texture with the atlas contents"""
        return self._texture

    @property
    def width(self) -> int:
        """int: Width of the atlas in pixels"""
        return self._width

    @property
    def height(self) -> int:
        """int: Height of the atlas in pixels"""
        return self._height

    @property
    def size(self) -> Tuple[int, int]:
        """Tuple[int, int]: The size of he atlas (width, height)"""
        return self._width, self._height

    def add(self, image: BaseImage):
        pass

    def remove(self, image: BaseImage):
        pass

    def resize(self, width: int, height: int):
        pass

    def rebuild(self):
        pass


class Allocator:
    """Row based allocator"""
    pass
