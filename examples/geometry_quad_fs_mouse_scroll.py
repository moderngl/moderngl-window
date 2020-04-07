from pathlib import Path

import moderngl_window
from moderngl_window import geometry
from moderngl_window import resources

resources.register_dir((Path(__file__).parent / 'resources').resolve())


class QuadFullscreenScroll(moderngl_window.WindowConfig):
    """Taking texture offset from mouse"""
    aspect_ratio = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quad = geometry.quad_fs()
        self.texture = self.load_texture_2d('textures/python-bg.png')
        self.prog = self.load_program('programs/texture_mouse_scroll.glsl')
        self.mouse_pos = 0, 0

    def render(self, time: float, frame_time: float):
        self.ctx.clear()

        self.texture.use(location=0)
        self.prog['texture0'] = 0
        self.prog['offset'] = -self.mouse_pos[0] / self.wnd.buffer_width, self.mouse_pos[1] / self.wnd.buffer_height
        self.quad.render(self.prog)

    def mouse_position_event(self, x, y, dx, dy):
        self.mouse_pos = self.mouse_pos[0] + dx, self.mouse_pos[1] + dy
        print(self.mouse_pos)


if __name__ == '__main__':
    moderngl_window.run_window_config(QuadFullscreenScroll)
