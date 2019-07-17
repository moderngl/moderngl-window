import moderngl

import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window import resources
from moderngl_window.meta import ProgramDescription
from moderngl_window.scene.camera import KeyboardCamera

from pyrr import matrix44


from base import CameraWindow


class GeometryBbox(CameraWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prog = resources.programs.load(ProgramDescription(path='scene_default/bbox.glsl'))
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
