import moderngl_window
from moderngl_window.text.bitmapped import TextWriter2D


class App(moderngl_window.WindowConfig):
    title = "Text"
    aspect_ratio = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.writer_quit = TextWriter2D()
        self.writer_quit.text = "Quit?"

        self.mode = "normal"  # normal / quit
        self.block_close = True

    def render(self, time, frame_time):
        if self.mode == "quit":
            self.writer_quit.draw((240, 380), size=120)

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys
        if self.mode == "quit":
            if key == keys.Y:
                self.block_close = False
                self.wnd.close()
            elif key == keys.N:
                self.block_close = True
                self.mode = "normal"

    def close(self, *args):
        if self.block_close:
            self.mode = "quit"
            self.wnd.is_closing = False


# Force running glfw window
moderngl_window.run_window_config(App, args=("--window", "glfw"))
