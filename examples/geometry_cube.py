from pathlib import Path
from pyrr import Matrix44, matrix44, Vector3

import moderngl

import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window import resources

from base import CameraWindow

resources.register_dir((Path(__file__).parent / 'resources').resolve())


class CubeSimple(CameraWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.cube = geometry.cube(size=(2, 2, 2))
        self.prog = self.load_program('programs/cube_simple.glsl')
        self.prog['m_proj'].write(self.camera.projection.tobytes())
        self.prog['color'].value = (1.0, 1.0, 1.0, 1.0)

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        m_rot = Matrix44.from_eulers(Vector3((time, time, time)))
        m_trans = matrix44.create_from_translation(Vector3((0.0, 0.0, -3.5)))
        m_mv = matrix44.multiply(m_rot, m_trans)

        self.prog['m_model'].write(m_mv.astype('f4').tobytes())
        self.prog['m_camera'].write(self.camera.matrix.astype('f4').tobytes())
        self.cube.render(self.prog)


if __name__ == '__main__':
    mglw.run_window_config(CubeSimple)
