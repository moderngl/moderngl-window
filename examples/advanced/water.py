import moderngl_window
from moderngl_window import geometry


class Water(moderngl_window.WindowConfig):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quad_fs = geometry.quad_fs()

        self.texture_1 = self.ctx.texture(self.wnd.buffer_size, components=3)
        self.texture_2 = self.ctx.texture(self.wnd.buffer_size, components=3)

        self.fbo_1 = self.ctx.framebuffer(color_attachments=[self.texture_1])
        self.fbo_2 = self.ctx.framebuffer(color_attachments=[self.texture_2])

    def render(self, time, frame_time):
        self.ctx.clear(1.0)


if __name__ == '__main__':
    moderngl_window.run_window_config(Water)
