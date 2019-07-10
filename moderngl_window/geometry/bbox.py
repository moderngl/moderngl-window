import numpy

import moderngl
from moderngl_window.opengl.vao import VAO


def bbox(width=1.0, height=1.0, depth=1.0):
    """
    Generates a bounding box with (0.0, 0.0, 0.0) as the center.
    This is simply a box with ``LINE_STRIP`` as draw mode.

    Keyword Args:
        width (float): Width of the box
        height (float): Height of the box
        depth (float): Depth of the box
    Returns:
        A :py:class:`moderngl_window.opengl.vao.VAO` instance
    """
    width, height, depth = width / 2.0, height / 2.0, depth / 2.0
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

    vao = VAO("geometry:cube", mode=moderngl.LINE_STRIP)
    vao.buffer(pos, '3f', ["in_position"])

    return vao
