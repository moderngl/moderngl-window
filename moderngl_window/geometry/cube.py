from typing import Optional

import numpy

from moderngl_window.geometry import AttributeNames
from moderngl_window.opengl.vao import VAO


def cube(
    size: tuple[float, float, float] = (1.0, 1.0, 1.0),
    center: tuple[float, float, float] = (0.0, 0.0, 0.0),
    normals: bool = True,
    uvs: bool = True,
    name: Optional[str] = None,
    attr_names: type[AttributeNames] = AttributeNames,
) -> VAO:
    """Creates a cube VAO with normals and texture coordinates

    Keyword Args:
        width (float): Width of the cube
        height (float): Height of the cube
        depth (float): Depth of the cube
        center: center of the cube as a 3-component tuple
        normals: (bool) Include normals
        uvs: (bool) include uv coordinates
        name (str): Optional name for the VAO
        attr_names (AttributeNames): Attribute names
    Returns:
        A :py:class:`moderngl_window.opengl.vao.VAO` instance
    """
    width, height, depth = size
    width, height, depth = width / 2.0, height / 2.0, depth / 2.0

    # fmt: off
    pos = numpy.array([
        center[0] + width, center[1] - height, center[2] + depth,
        center[0] + width, center[1] + height, center[2] + depth,
        center[0] - width, center[1] - height, center[2] + depth,
        center[0] + width, center[1] + height, center[2] + depth,
        center[0] - width, center[1] + height, center[2] + depth,
        center[0] - width, center[1] - height, center[2] + depth,
        center[0] + width, center[1] - height, center[2] - depth,
        center[0] + width, center[1] + height, center[2] - depth,
        center[0] + width, center[1] - height, center[2] + depth,
        center[0] + width, center[1] + height, center[2] - depth,
        center[0] + width, center[1] + height, center[2] + depth,
        center[0] + width, center[1] - height, center[2] + depth,
        center[0] + width, center[1] - height, center[2] - depth,
        center[0] + width, center[1] - height, center[2] + depth,
        center[0] - width, center[1] - height, center[2] + depth,
        center[0] + width, center[1] - height, center[2] - depth,
        center[0] - width, center[1] - height, center[2] + depth,
        center[0] - width, center[1] - height, center[2] - depth,
        center[0] - width, center[1] - height, center[2] + depth,
        center[0] - width, center[1] + height, center[2] + depth,
        center[0] - width, center[1] + height, center[2] - depth,
        center[0] - width, center[1] - height, center[2] + depth,
        center[0] - width, center[1] + height, center[2] - depth,
        center[0] - width, center[1] - height, center[2] - depth,
        center[0] + width, center[1] + height, center[2] - depth,
        center[0] + width, center[1] - height, center[2] - depth,
        center[0] - width, center[1] - height, center[2] - depth,
        center[0] + width, center[1] + height, center[2] - depth,
        center[0] - width, center[1] - height, center[2] - depth,
        center[0] - width, center[1] + height, center[2] - depth,
        center[0] + width, center[1] + height, center[2] - depth,
        center[0] - width, center[1] + height, center[2] - depth,
        center[0] + width, center[1] + height, center[2] + depth,
        center[0] - width, center[1] + height, center[2] - depth,
        center[0] - width, center[1] + height, center[2] + depth,
        center[0] + width, center[1] + height, center[2] + depth,
    ], dtype=numpy.float32)

    if normals:
        normal_data = numpy.array([
            -0, 0, 1,
            -0, 0, 1,
            -0, 0, 1,
            0, 0, 1,
            0, 0, 1,
            0, 0, 1,
            1, 0, 0,
            1, 0, 0,
            1, 0, 0,
            1, 0, 0,
            1, 0, 0,
            1, 0, 0,
            0, -1, 0,
            0, -1, 0,
            0, -1, 0,
            0, -1, 0,
            0, -1, 0,
            0, -1, 0,
            -1, -0, 0,
            -1, -0, 0,
            -1, -0, 0,
            -1, -0, 0,
            -1, -0, 0,
            -1, -0, 0,
            0, 0, -1,
            0, 0, -1,
            0, 0, -1,
            0, 0, -1,
            0, 0, -1,
            0, 0, -1,
            0, 1, 0,
            0, 1, 0,
            0, 1, 0,
            0, 1, 0,
            0, 1, 0,
            0, 1, 0,
        ], dtype=numpy.float32)

    if uvs:
        uvs_data = numpy.array([
            1, 0,
            1, 1,
            0, 0,
            1, 1,
            0, 1,
            0, 0,
            1, 0,
            1, 1,
            0, 0,
            1, 1,
            0, 1,
            0, 0,
            1, 1,
            0, 1,
            0, 0,
            1, 1,
            0, 0,
            1, 0,
            0, 1,
            0, 0,
            1, 0,
            0, 1,
            1, 0,
            1, 1,
            1, 0,
            1, 1,
            0, 1,
            1, 0,
            0, 1,
            0, 0,
            1, 1,
            0, 1,
            1, 0,
            0, 1,
            0, 0,
            1, 0
        ], dtype=numpy.float32)
    # fmt: on

    vao = VAO(name or "geometry:cube")

    # Add buffers
    vao.buffer(pos, "3f", [attr_names.POSITION])
    if normals:
        vao.buffer(normal_data, "3f", [attr_names.NORMAL])
    if uvs:
        vao.buffer(uvs_data, "2f", [attr_names.TEXCOORD_0])

    return vao
