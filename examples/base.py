import moderngl_window as mglw
from moderngl_window.scene.camera import KeyboardCamera


class CameraWindow(mglw.WindowConfig):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = KeyboardCamera(self.wnd.keys, aspect_ratio=self.wnd.aspect_ratio)

    def key_event(self, key, action, modifiers):
        self.camera.key_input(key, action, modifiers)

        if key == self.wnd.keys.SPACE and action == self.wnd.keys.ACTION_PRESS:
            self.timer.toggle_pause()

    def mouse_position_event(self, x: int, y: int, dx, dy):
        self.camera.rot_state(dx, dy)

    def resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)
