from pathlib import Path

import moderngl_window
from moderngl_window import geometry
from moderngl_window import resources
from moderngl_window.meta import TextureDescription, ProgramDescription

resources.register_dir((Path(__file__).parent / 'resources').resolve())


class QuadFullscreen(moderngl_window.WindowConfig):
    aspect_ratio = 1980 / 1024

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quad = geometry.quad_fs()
        self.texture = resources.textures.load(TextureDescription(path='textures/python-bg.png'))
        self.prog = resources.programs.load(ProgramDescription(path='programs/texture.glsl'))

    def render(self, time: float, frame_time: float):
        self.ctx.screen.clear()

        # self.texture.use(location=0)
        self.prog['texture0'].value = 0
        self.quad.render(self.prog)


if __name__ == '__main__':
    moderngl_window.run_window_config(QuadFullscreen)
