import random
from pathlib import Path
import numpy as np

import moderngl
import moderngl_window
from moderngl_window import geometry
from moderngl_window import screenshot


class Water(moderngl_window.WindowConfig):
    title = "Water"
    resource_dir = (Path(__file__) / '../../resources').absolute()
    aspect_ratio = None  # We'll do manual viewport for now
    window_size = 1024, 1024
    resizable = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = self.wnd.buffer_size
        self.viewport = (0, 0, self.size[0], self.size[1])

        self.quad_fs = geometry.quad_fs()
        self.sprite = geometry.quad_2d(size=(9 / self.size[0], 9 / self.size[1]))

        self.texture_1 = self.ctx.texture(self.size, components=3)
        self.texture_2 = self.ctx.texture(self.size, components=3)

        self.fbo_1 = self.ctx.framebuffer(color_attachments=[self.texture_1])
        self.fbo_1.viewport = self.viewport
        self.fbo_2 = self.ctx.framebuffer(color_attachments=[self.texture_2])
        self.fbo_2.viewport = self.viewport

        drop = np.array([[0.0, 0.0, 1/6, 1/5, 1/4, 1/5, 1/6, 0.0, 0.0],
                         [0.0, 1/6, 1/5, 1/4, 1/3, 1/4, 1/5, 1/6, 0.0],
                         [1/6, 1/5, 1/4, 1/3, 1/2, 1/3, 1/4, 1/5, 1/6],
                         [1/5, 1/4, 1/3, 1/2, 1.0, 1/2, 1/3, 1/4, 1/5],
                         [1/4, 1/3, 1/2, 1.0, 1.0, 1.0, 1/2, 1/3, 1/4],
                         [1/5, 1/4, 1/3, 1/2, 1.0, 1/2, 1/3, 1/4, 1/5],
                         [1/6, 1/5, 1/4, 1/3, 1/2, 1/3, 1/4, 1/5, 1/6],
                         [0.0, 1/6, 1/5, 1/4, 1/3, 1/4, 1/5, 1/6, 0.0],
                         [0.0, 0.0, 1/6, 1/5, 1/4, 1/5, 1/6, 0.0, 0.0]])
        self.drops_texture = self.ctx.texture((9, 9), components=1, dtype='f4')
        self.drops_texture.write(drop.astype('f4').tobytes())

        # programs
        self.drop_program = self.load_program('programs/water/drop.glsl')
        self.wave_program = self.load_program('programs/water/wave.glsl')
        self.wave_program['texture0'].value = 0
        self.wave_program['texture1'].value = 1

        self.mouse_pos = 0, 0

    def render(self, time, frame_time):
        self.ctx.viewport = self.viewport

        self.fbo_2.use()

        # Render drop (with additive blending) when mouse is pressed
        if self.wnd.mouse_states.any:
            self.ctx.enable(moderngl.BLEND)
            self.ctx.blend_func = moderngl.ONE, moderngl.ONE
            self.drops_texture.use()
            self.drop_program['pos'].value = self.mouse_pos
            self.sprite.render(self.drop_program)
            self.ctx.disable(moderngl.BLEND)

        # HACK: Just draw 100 new drops per frame (copy paste from above)
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.ONE, moderngl.ONE
        self.drops_texture.use()
        for i in range(25):
            self.drop_program['pos'].value = random.random() * 2 - 1.0, random.random() * 2 - 1
            self.sprite.render(self.drop_program)
        self.ctx.disable(moderngl.BLEND)

        self.fbo_1.use()

        # Process the water
        self.texture_2.use(location=0)
        self.texture_1.use(location=1)
        self.quad_fs.render(self.wave_program)

        self.ctx.copy_framebuffer(self.ctx.screen, self.fbo_1)

        # Swapperoo
        self.texture_1, self.texture_2 = self.texture_2, self.texture_1
        self.fbo_1, self.fbo_2 = self.fbo_2, self.fbo_1

    def mouse_position_event(self, x, y, dx, dy):
        self.mouse_pos = x * 2 / self.size[0] - 1.0, -y * 2 / self.size[1] + 1.0

    def mouse_drag_event(self, x, y, dx, dy):
        self.mouse_position_event(x, y, dx, dy)

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        # Key presses
        if action == keys.ACTION_PRESS:
            if key == keys.F1:
                screenshot.create(self.fbo_1)


if __name__ == '__main__':
    moderngl_window.run_window_config(Water)
