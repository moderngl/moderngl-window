"""
Simple row based texture atlas created for fast runtime allocation.

* This atlas is partly based on the texture atlas in the Arcade project
* The allocator is based on Pyglet's row allocator

https://github.com/pyglet/pyglet/blob/master/pyglet/image/atlas.py
https://github.com/pythonarcade/arcade/blob/development/arcade/texture_atlas.py
"""

from typing import Tuple

import moderngl
from .base import BaseImage


class AllocatorException(Exception):
    pass


class _Row:
    """
    A row in the texture atlas.
    """
    __slots__ = ("x", "y", "y2", "max_height")

    def __init__(self, y: int, max_height: int) -> None:
        self.x = 0
        self.y = y
        self.max_height = max_height
        self.y2 = y

    def add(self, width: int, height: int) -> Tuple[int, int]:
        """Add a region to the row and return the position"""
        if width <= 0 or height <= 0:
            raise AllocatorException("Cannot allocate size: [{}, {}]".format(width, height))
        if height > self.max_height:
            raise AllocatorException("Cannot allocate past the max height")

        x, y = self.x, self.y
        self.x += width
        # Keep track of the highest y value for compaction
        self.y2 = max(self.y + height, self.y2)
        return x, y

    def compact(self):
        """
        Compacts the row to the smallest height.
        Should only be done once when the row is filled before adding a new row.
        """
        self.max_height = self.y2 - self.y


class Allocator:
    """Row based allocator"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # First row covers the entire height until compacted
        # when a new row is added
        self.rows = [_Row(0, self.height)]

    def alloc(self, width: int, height: int) -> Tuple[int, int]:
        """
        Allocate a region.

        Returns:
            Tuple[int, int]: The x,y location
        Raises:
            AllocatorException: if no more space
        """
        # Check if we have room in existing rows
        for row in self.rows:
            # Can we add the region to the end if this row?
            if self.width - row.x >= width and row.max_height >= height:
                return row.add(width, height)

        # Can we make a new row?
        if self.width >= width and self.height - row.y2 >= height:
            # Compact the last row
            row.compact()
            # New row continuing from y2 with a remaining of the height as the max
            new_row = _Row(row.y2, self.height - row.y2)
            self.rows.append(new_row)
            # Allocate the are in the new row
            return new_row.add(width, height)

        raise AllocatorException("No more space in {} for box [{}, {}]".format(self, width, height))


class TextureAtlas:
    """
    A simple texture atlas using a row based allocation.
    There are more efficient ways to pack textures, but this
    is normally sufficient for dynamic atlases were textures
    are added on the fly runtime.
    """
    def __init__(
        self,
        ctx: moderngl.Context,
        width: int,
        height: int,
        components: int = 4,
        border: int = 1,
        auto_resize: bool = True,
    ):
        # Basic properties
        self._ctx = ctx
        self._width = width
        self._height = height
        self._components = components
        self._border = border
        self._auto_resize = auto_resize

        # The physical size limit for the current hardware
        self._max_size = self._ctx.info["GL_MAX_VIEWPORT_DIMS"]

        # Atlas content
        self._texture = self._ctx.texture(self.size, components=self._components)

        # We want to be able to render into the atlas texture
        self._fbo = self._fbo = self._ctx.framebuffer(
            color_attachments=[self._texture]
        )
        self._allocator = Allocator(width, height)

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

    @property
    def max_size(self) -> Tuple[int, int]:
        """
        Tuple[int,int]: The maximum size of the atlas in pixels (x, y)
        """
        return self._max_size

    def add(self, image: BaseImage):
        pass

    def remove(self, image: BaseImage):
        pass

    def resize(self, width: int, height: int):
        pass

    def rebuild(self):
        pass
