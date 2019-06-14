import numpy

from moderngl_window.opengl.vao import VAO


def cube(size=(1.0, 1.0, 1.0), center=(0.0, 0.0, 0.0), normals=True, uvs=True) -> VAO:
    """
    Creates a cube VAO with normals and texture coordinates
    Args:
        width (float): Width of the cube
        height (float): Height of the cube
        depth (float): Depth of the cube
    Keyword Args:
        center: center of the cube as a 3-component tuple
        normals: (bool) Include normals
        uvs: (bool) include uv coordinates
    Returns:
        A :py:class:`moderngl_window.opengl.vao.VAO` instance
    """
    width, height, depth = size
    width, height, depth = width / 2.0, height / 2.0, depth / 2.0

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

    vao = VAO("geometry:cube")

    # Add buffers
    vao.buffer(pos, '3f', ['in_position'])
    if normals:
        vao.buffer(normal_data, '3f', ['in_normal'])
    if uvs:
        vao.buffer(uvs_data, '2f', ['in_uv'])

    return vao
