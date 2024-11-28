from typing import Optional

import moderngl
import numpy

from moderngl_window.geometry import AttributeNames
from moderngl_window.opengl.vao import VAO


def bbox(
    size: tuple[float, float, float] = (1.0, 1.0, 1.0),
    name: Optional[str] = None,
    attr_names: type[AttributeNames] = AttributeNames,
) -> VAO:
    """
    Generates a bounding box with (0.0, 0.0, 0.0) as the center.
    This is simply a box with ``LINE_STRIP`` as draw mode.

    Keyword Args:
        size (tuple): x, y, z size of the box
        name (str): Optional name for the VAO
        attr_names (AttributeNames): Attribute names
    Returns:
        A :py:class:`moderngl_window.opengl.vao.VAO` instance
    """
    width, height, depth = size[0] / 2.0, size[1] / 2.0, size[2] / 2.0
    # fmt: off
    pos = numpy.array([
        width, -height, depth,
        width, height, depth,
        -width, -height, depth,
        width, height, depth,
        -width, height, depth,
        -width, -height, depth,
        width, -height, -depth,
        width, height, -depth,
        width, -height, depth,
        width, height, -depth,
        width, height, depth,
        width, -height, depth,
        width, -height, -depth,
        width, -height, depth,
        -width, -height, depth,
        width, -height, -depth,
        -width, -height, depth,
        -width, -height, -depth,
        -width, -height, depth,
        -width, height, depth,
        -width, height, -depth,
        -width, -height, depth,
        -width, height, -depth,
        -width, -height, -depth,
        width, height, -depth,
        width, -height, -depth,
        -width, -height, -depth,
        width, height, -depth,
        -width, -height, -depth,
        -width, height, -depth,
        width, height, -depth,
        -width, height, -depth,
        width, height, depth,
        -width, height, -depth,
        -width, height, depth,
        width, height, depth,
    ], dtype=numpy.float32)
    # fmt: on

    vao = VAO(name or "geometry:cube", mode=moderngl.LINE_STRIP)
    vao.buffer(pos, "3f", [attr_names.POSITION])

    return vao
