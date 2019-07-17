import numpy

import moderngl
from moderngl_window.opengl.vao import VAO
from moderngl_window.geometry.attributes import AttributeNames


def quad_fs(attrib_names=AttributeNames, normals=True, uvs=True, name=None) -> VAO:
    """
    Creates a screen aligned quad using two triangles with normals and texture coordiantes.

    Keyword Args:
        attrib_names (AttributeNames): Attrib name config
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
        attrib_names=attrib_names,
        name=name,
    )


def quad_2d(width=1.0, height=1.0, xpos=0.0, ypos=0.0,
            normals=True, uvs=True, attrib_names=AttributeNames, name=None) -> VAO:
    """
    Creates a 2D quad VAO using 2 triangles with normals and texture coordinates.

    Keyword Args:
        width (float): Width of the quad
        height (float): Height of the quad
        xpos (float): Center position x
        ypos (float): Center position y
        name (str): Optional name for the VAO
    Returns:
        A :py:class:`VAO` instance.
    """
    pos = numpy.array([
        xpos - width / 2.0, ypos + height / 2.0, 0.0,
        xpos - width / 2.0, ypos - height / 2.0, 0.0,
        xpos + width / 2.0, ypos - height / 2.0, 0.0,
        xpos - width / 2.0, ypos + height / 2.0, 0.0,
        xpos + width / 2.0, ypos - height / 2.0, 0.0,
        xpos + width / 2.0, ypos + height / 2.0, 0.0,
    ], dtype=numpy.float32)

    normals = numpy.array([
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
    ], dtype=numpy.float32)

    uvs = numpy.array([
        0.0, 1.0,
        0.0, 0.0,
        1.0, 0.0,
        0.0, 1.0,
        1.0, 0.0,
        1.0, 1.0,
    ], dtype=numpy.float32)

    vao = VAO(name or "geometry:quad", mode=moderngl.TRIANGLES)
    vao.buffer(pos, '3f', [attrib_names.POSITION])
    if normals:
        vao.buffer(normals, '3f', [attrib_names.NORMAL])
    if uvs:
        vao.buffer(uvs, '2f', [attrib_names.TEXCOORD_0])

    return vao
