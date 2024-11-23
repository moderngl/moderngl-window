import numpy

import moderngl
from moderngl_window.opengl.vao import VAO
from moderngl_window.geometry.attributes import AttributeNames


def quad_fs(attr_names=AttributeNames, normals=True, uvs=True, name=None) -> VAO:
    """
    Creates a screen aligned quad using two triangles with normals and texture coordinates.

    Keyword Args:
        attr_names (AttributeNames): Attrib name config
        normals (bool): Include normals in VAO
        uvs (bool): Include texture coordinates in VAO
        name (str): Optional name for the VAO
    Returns:
        A :py:class:`~moderngl_window.opengl.vao.VAO` instance.
    """
    return quad_2d(
        size=(2.0, 2.0),
        normals=normals,
        uvs=uvs,
        attr_names=attr_names,
        name=name,
    )


def quad_2d(
    size=(1.0, 1.0),
    pos=(0.0, 0.0),
    normals=True,
    uvs=True,
    attr_names=AttributeNames,
    name=None,
) -> VAO:
    """
    Creates a 2D quad VAO using 2 triangles with normals and texture coordinates.

    Keyword Args:
        size (tuple): width and height
        pos (float): Center position x and y
        normals (bool): Include normals in VAO
        uvs (bool): Include texture coordinates in VAO
        attr_names (AttributeNames): Attrib name config
        name (str): Optional name for the VAO
    Returns:
        A :py:class:`~moderngl_window.opengl.vao.VAO` instance.
    """
    width, height = size
    xpos, ypos = pos

    # fmt: off
    pos_data = numpy.array([
        xpos - width / 2.0, ypos + height / 2.0, 0.0,
        xpos - width / 2.0, ypos - height / 2.0, 0.0,
        xpos + width / 2.0, ypos - height / 2.0, 0.0,
        xpos - width / 2.0, ypos + height / 2.0, 0.0,
        xpos + width / 2.0, ypos - height / 2.0, 0.0,
        xpos + width / 2.0, ypos + height / 2.0, 0.0,
    ], dtype=numpy.float32)

    normal_data = numpy.array([
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
    ], dtype=numpy.float32)

    uv_data = numpy.array([
        0.0, 1.0,
        0.0, 0.0,
        1.0, 0.0,
        0.0, 1.0,
        1.0, 0.0,
        1.0, 1.0,
    ], dtype=numpy.float32)
    # fmt: on

    vao = VAO(name or "geometry:quad", mode=moderngl.TRIANGLES)
    vao.buffer(pos_data, "3f", [attr_names.POSITION])
    if normals:
        vao.buffer(normal_data, "3f", [attr_names.NORMAL])
    if uvs:
        vao.buffer(uv_data, "2f", [attr_names.TEXCOORD_0])

    return vao
