from pathlib import Path
import numpy as np
import moderngl_window
from moderngl_window import geometry


class Water(moderngl_window.WindowConfig):
    title = "Water"
    resource_dir = (Path(__file__) / '../../resources').absolute()
    aspect_ratio = 1.0
    window_size = 1024, 1024
    resizable = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = self.window_size

        self.quad_fs = geometry.quad_fs()
        self.sprite = geometry.quad_2d(size=(0.1, 0.1))

        self.texture_1 = self.ctx.texture(self.size, components=3)
        self.texture_2 = self.ctx.texture(self.size, components=3)

        self.fbo_1 = self.ctx.framebuffer(color_attachments=[self.texture_1])
        self.fbo_2 = self.ctx.framebuffer(color_attachments=[self.texture_2])

        drop = np.array([[0.0, 0.0, 1/6, 1/5, 1/4, 1/5, 1/6, 0.0, 0.0],
                        [0.0, 1/6, 1/5, 1/4, 1/3, 1/4, 1/5, 1/6, 0.0],
                        [1/6, 1/5, 1/4, 1/3, 1/2, 1/3, 1/4, 1/5, 1/6],
                        [1/5, 1/2, 1/3, 1/2, 1.0, 1/2, 1/3, 1/4, 1/5],
                        [1/4, 1/3, 1/2, 1.0, 1.0, 1.0, 1/2, 1/3, 1/4],
                        [1/5, 1/2, 1/3, 1/2, 1.0, 1/2, 1/3, 1/4, 1/5],
                        [1/6, 1/5, 1/4, 1/3, 1/2, 1/3, 1/4, 1/5, 1/6],
                        [0.0, 1/6, 1/5, 1/4, 1/3, 1/4, 1/5, 1/6, 0.0],
                        [0.0, 0.0, 1/6, 1/5, 1/4, 1/5, 1/6, 0.0, 0.0]])
        self.drops_texture = self.ctx.texture((9, 9), components=1, dtype='f4')
        self.drops_texture.write(drop.astype('f4').tobytes())

        # programs
        self.drop_program = self.load_program('programs/water/drop.glsl')
        # self.wave_program = self.load_program('programs/water/wave.glsl')
        self.mouse_pos = 0, 0

    def render(self, time, frame_time):
        self.ctx.viewport = (0, 0, self.size[0], self.size[1])

        self.drops_texture.use()
        self.drop_program['pos'].value = self.mouse_pos
        self.sprite.render(self.drop_program)

    def mouse_position_event(self, x, y, dx, dy):
        self.mouse_pos = x * 2 / self.size[0] - 1.0, -y * 2 / self.size[1] + 1.0


if __name__ == '__main__':
    moderngl_window.run_window_config(Water)
