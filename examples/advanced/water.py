from pathlib import Path
import numpy as np
import moderngl_window
from moderngl_window import geometry


class Water(moderngl_window.WindowConfig):
    title = "Water"
    resource_dir = (Path(__file__) / '../../resources').absolute()
    aspect_ratio = 1.0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quad_fs = geometry.quad_fs()
        # self.sprite = geometry.quad_2d(size=)

        self.size = (256, 256)

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

    def render(self, time, frame_time):

        self.drops_texture.use()
        self.quad_fs.render(self.drop_program)


if __name__ == '__main__':
    moderngl_window.run_window_config(Water)
