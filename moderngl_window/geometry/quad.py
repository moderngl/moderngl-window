import numpy

import moderngl
from moderngl_window.opengl.vao import VAO
from moderngl_window.geometry.attributes import AttributeNames


def quad_fs(attr_names=AttributeNames, normals=True, uvs=True, name=None) -> VAO:
    """
    Creates a screen aligned quad using two triangles with normals and texture coordiantes.

    Keyword Args:
        attr_names (AttributeNames): Attrib name config
        normals (bool): Include normals in VAO
        uvs (bool): Include normals in VAO
        name (str): Optional name for the VAO
    Returns:
        A :py:class:`demosys.opengl.vao.VAO` instance.
    """
    return quad_2d(
        width=2.0,
        height=2.0,
        xpos=0.0,
        ypos=0.0,
        normals=normals,
        uvs=uvs,
        attr_names=attr_names,
        name=name,
    )


def quad_2d(width=1.0, height=1.0, xpos=0.0, ypos=0.0,
            normals=True, uvs=True, attr_names=AttributeNames, name=None) -> VAO:
    """
    Creates a 2D quad VAO using 2 triangles with normals and texture coordinates.

    Keyword Args:
        width (float): Width of the quad
        height (float): Height of the quad
        xpos (float): Center position x
        ypos (float): Center position y
        normals (bool): Include normals in VAO
        uvs (bool): Include normals in VAO
        attr_names (AttributeNames): Attrib name config
        name (str): Optional name for the VAO
    Returns:
        A :py:class:`VAO` instance.
    """
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

    vao = VAO(name or "geometry:quad", mode=moderngl.TRIANGLES)
    vao.buffer(pos_data, '3f', [attr_names.POSITION])
    if normals:
        vao.buffer(normal_data, '3f', [attr_names.NORMAL])
    if uvs:
        vao.buffer(uv_data, '2f', [attr_names.TEXCOORD_0])

    return vao
