from pathlib import Path

import moderngl_window
from moderngl_window import geometry, resources

resources.register_dir((Path(__file__).parent / "resources").resolve())


class QuadFullscreen(moderngl_window.WindowConfig):
    title = "Quad Fullscreen"
    window_size = 1980, 1024
    aspect_ratio = 1980 / 1024

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quad = geometry.quad_fs()
        self.texture = self.load_texture_2d("textures/python-bg.png")
        self.prog = self.load_program("programs/texture.glsl")

    def on_render(self, time: float, frame_time: float):
        self.ctx.clear()

        self.texture.use(location=0)
        self.prog["texture0"].value = 0
        self.quad.render(self.prog)


if __name__ == "__main__":
    moderngl_window.run_window_config(QuadFullscreen)
