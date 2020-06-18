"""
A example showing how you can switch between windowed and fullscreen
"""
import moderngl_window as mglw


class FullscreenSwitching(mglw.WindowConfig):
    # moderngl_window settings
    title = "fullscreen-switching"

    def render(self, time: float, frame_time: float) -> None:
        pass

    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.F11:
                print('switching fs')
                self.wnd.fullscreen = not self.wnd.fullscreen


if __name__ == "__main__":
    FullscreenSwitching.run()
