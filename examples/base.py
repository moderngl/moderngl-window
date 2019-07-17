import moderngl

import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window import resources
from moderngl_window.meta import ProgramDescription
from moderngl_window.scene.camera import KeyboardCamera

from pyrr import matrix44


class CameraWindow(mglw.WindowConfig):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = KeyboardCamera(self.wnd.keys, aspect=self.wnd.aspect_ratio)

    def key_event(self, key, action, modifiers):
        self.camera.key_input(key, action, modifiers)

        if key == self.wnd.keys.SPACE and action == self.wnd.keys.ACTION_PRESS:
            self.timer.toggle_pause()

    def mouse_position_event(self, x: int, y: int):
        self.camera.rot_state(x, y)

    def resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)
