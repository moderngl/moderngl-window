from pyrr import matrix44

import moderngl_window as mglw
from moderngl_window import geometry

from base import CameraWindow


class GeometryBbox(CameraWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prog = self.load_program('scene_default/bbox.glsl')
        self.bbox = geometry.bbox()

        self.prog['color'].value = (1, 1, 1)
        self.prog['bb_min'].value = (-2, -2, -2)
        self.prog['bb_max'].value = (2, 2, 2)
        self.prog['m_model'].write(matrix44.create_from_translation([0.0, 0.0, -8.0], dtype='f4'))

    def render(self, time: float, frame_time: float):
        self.ctx.clear()

        self.prog['m_proj'].write(self.camera.projection.tobytes())
        self.prog['m_cam'].write(self.camera.matrix.astype('f4').tobytes())
        self.bbox.render(self.prog)


if __name__ == '__main__':
    mglw.run_window_config(GeometryBbox)
