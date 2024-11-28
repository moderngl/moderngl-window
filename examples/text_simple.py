import moderngl_window
from moderngl_window.text.bitmapped import TextWriter2D


class App(moderngl_window.WindowConfig):
    title = "Text"
    aspect_ratio = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.writer = TextWriter2D()
        self.writer.text = "Hello ModernGL!"

    def on_render(self, time, frame_time):
        self.writer.draw((240, 380), size=120)


App.run()
