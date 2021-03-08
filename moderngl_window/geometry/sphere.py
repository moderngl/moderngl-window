import math

import numpy

import moderngl as mlg
from moderngl_window.opengl.vao import VAO
from moderngl_window.geometry import AttributeNames


def sphere(
    radius=0.5,
    sectors=32,
    rings=16,
    normals=True,
    uvs=True,
    name: str = None,
    attr_names=AttributeNames,
) -> VAO:
    """Creates a sphere.

    Keyword Args:
        radius (float): Radius or the sphere
        rings (int): number or horizontal rings
        sectors (int): number of vertical segments
        normals (bool): Include normals in the VAO
        uvs (bool): Include texture coordinates in the VAO
        name (str): An optional name for the VAO
        attr_names (AttributeNames): Attribute names
    Returns:
        A :py:class:`VAO` instance
    """
    R = 1.0 / (rings - 1)
    S = 1.0 / (sectors - 1)

    vertices = [0] * (rings * sectors * 3)
    normals = [0] * (rings * sectors * 3)
    uvs = [0] * (rings * sectors * 2)

    v, n, t = 0, 0, 0
    for r in range(rings):
        for s in range(sectors):
            y = math.sin(-math.pi / 2 + math.pi * r * R)
            x = math.cos(2 * math.pi * s * S) * math.sin(math.pi * r * R)
            z = math.sin(2 * math.pi * s * S) * math.sin(math.pi * r * R)

            uvs[t] = s * S
            uvs[t + 1] = r * R

            vertices[v] = x * radius
            vertices[v + 1] = y * radius
            vertices[v + 2] = z * radius

            normals[n] = x
            normals[n + 1] = y
            normals[n + 2] = z

            t += 2
            v += 3
            n += 3

    indices = [0] * rings * sectors * 6
    i = 0
    for r in range(rings - 1):
        for s in range(sectors - 1):
            indices[i] = r * sectors + s
            indices[i + 1] = (r + 1) * sectors + (s + 1)
            indices[i + 2] = r * sectors + (s + 1)

            indices[i + 3] = r * sectors + s
            indices[i + 4] = (r + 1) * sectors + s
            indices[i + 5] = (r + 1) * sectors + (s + 1)
            i += 6

    vao = VAO(name or "sphere", mode=mlg.TRIANGLES)

    vbo_vertices = numpy.array(vertices, dtype=numpy.float32)
    vao.buffer(vbo_vertices, "3f", [attr_names.POSITION])

    if normals:
        vbo_normals = numpy.array(normals, dtype=numpy.float32)
        vao.buffer(vbo_normals, "3f", [attr_names.NORMAL])

    if uvs:
        vbo_uvs = numpy.array(uvs, dtype=numpy.float32)
        vao.buffer(vbo_uvs, "2f", [attr_names.TEXCOORD_0])

    vbo_elements = numpy.array(indices, dtype=numpy.uint32)
    vao.index_buffer(vbo_elements, index_element_size=4)

    return vao
