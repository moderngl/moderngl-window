import math

from OpenGL import GL

import moderngl_window


class PyOpenGL(moderngl_window.WindowConfig):
    gl_version = (3, 3)
    title = "PyOpenGL"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_render(self, time, frametime):
        GL.glClearColor(
            (math.sin(time) + 1.0) / 2,
            (math.sin(time + 2) + 1.0) / 2,
            (math.sin(time + 3) + 1.0) / 2,
            1.0,
        )
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)


if __name__ == "__main__":
    PyOpenGL.run()
