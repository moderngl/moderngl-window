import math

import moderngl_window


class BasicWindowConfig(moderngl_window.WindowConfig):
    """Minimal WindowConfig example"""
    gl_version = (3, 3)
    title = "Basic Window Config"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, time, frametime):
        self.ctx.clear(
            (math.sin(time) + 1.0) / 2,
            (math.sin(time + 2) + 1.0) / 2,
            (math.sin(time + 3) + 1.0) / 2,
        )


if __name__ == '__main__':
    moderngl_window.run_window_config(BasicWindowConfig)
