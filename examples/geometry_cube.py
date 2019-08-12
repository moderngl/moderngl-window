from pathlib import Path
from pyrr import Matrix44, matrix44, Vector3

import moderngl

import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window import resources
from moderngl_window.meta import ProgramDescription

from base import CameraWindow

resources.register_dir((Path(__file__).parent / 'resources').resolve())


class CubeSimple(CameraWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cube = geometry.cube(size=(2, 2, 2))
        self.prog = resources.programs.load(ProgramDescription(path='programs/cube_simple.glsl'))
        self.prog['m_proj'].write(self.camera.projection.tobytes())
        self.prog['color'].value = (1.0, 1.0, 1.0, 1.0)
        self.scope = self.ctx.scope(self.ctx.CULL_FACE | self.ctx.DEPTH_TEST)

    def render(self, time: float, frametime: float):
        m_rot = Matrix44.from_eulers(Vector3((time, time, time)))
        m_trans = matrix44.create_from_translation(Vector3((0.0, 0.0, -3.0)))
        m_mv = matrix44.multiply(m_rot, m_trans)

        self.prog['m_model'].write(m_mv.astype('f4').tobytes())
        self.prog['m_camera'].write(self.camera.matrix.astype('f4').tobytes())
        self.cube.render(self.prog, self.scope)


if __name__ == '__main__':
    mglw.run_window_config(CubeSimple)
