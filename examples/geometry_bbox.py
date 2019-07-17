import moderngl

import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window import resources
from moderngl_window.meta import ProgramDescription
from moderngl_window.scene.camera import KeyboardCamera

from pyrr import matrix44


class GeometryBbox(mglw.WindowConfig):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prog = resources.programs.load(ProgramDescription(path='scene_default/bbox.glsl'))
        self.bbox = geometry.bbox()
        self.camera = KeyboardCamera(self.wnd.keys, aspect=self.wnd.aspect_ratio)

        self.prog['color'].value = (1, 1, 1)

        self.prog['bb_min'].value = (-2, -2, -2)
        self.prog['bb_max'].value = (2, 2, 2)

        self.prog['m_model'].write(matrix44.create_from_translation([0.0, 0.0, -8.0], dtype='f4'))

    def render(self, time: float, frame_time: float):
        self.ctx.clear()

        self.prog['m_proj'].write(self.camera.projection.tobytes())
        self.prog['m_cam'].write(self.camera.matrix.astype('f4').tobytes())
        self.bbox.render(self.prog)

    def key_event(self, key, action, modifiers):
        self.camera.key_input(key, action, modifiers)

    def mouse_position_event(self, x: int, y: int):
        self.camera.rot_state(x, y)

    def resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)


if __name__ == '__main__':
    mglw.run_window_config(GeometryBbox)
