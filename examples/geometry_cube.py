from pathlib import Path
from pyrr import Matrix44, Vector3

import moderngl
import moderngl_window
from moderngl_window import geometry

from base import CameraWindow


class CubeSimple(CameraWindow):
    title = "Plain Cube"
    resource_dir = (Path(__file__).parent / 'resources').resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.cube = geometry.cube(size=(2, 2, 2))
        self.prog = self.load_program('programs/cube_simple.glsl')
        self.prog['color'].value = 1.0, 1.0, 1.0, 1.0

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        rotation = Matrix44.from_eulers((time, time, time), dtype='f4')
        translation = Matrix44.from_translation((0.0, 0.0, -3.5), dtype='f4')
        modelview = translation * rotation

        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_model'].write(modelview)
        self.prog['m_camera'].write(self.camera.matrix)

        self.cube.render(self.prog)


if __name__ == '__main__':
    moderngl_window.run_window_config(CubeSimple)
