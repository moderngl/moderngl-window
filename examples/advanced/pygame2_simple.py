"""
Based on BlubberQuark's blog:
https://blubberquark.tumblr.com/post/185013752945/using-moderngl-for-post-processing-shaders-with

Clears the screen using opengl with a constantly changing
color value and alpha blend a pygame surface on top.
"""
import math
from pathlib import Path
import pygame
import moderngl
import moderngl_window
from moderngl_window import geometry


class Pygame(moderngl_window.WindowConfig):
    """
    Example using pygame with moderngl.
    Needs to run with ``--window pygame2`` option.
    """
    title = "Pygame"
    window_size = 1280, 720
    resource_dir = (Path(__file__) / '../../resources').absolute()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.wnd.name != 'pygame2':
            raise RuntimeError('This example only works with --window pygame2 option')

        self.pg_res = (320, 180)
        # Create a 24bit (rgba) offscreen surface pygame can render to
        self.pg_screen = pygame.Surface(self.pg_res, flags=pygame.SRCALPHA)
        # 24 bit (rgba) moderngl texture
        self.pg_texture = self.ctx.texture(self.pg_res, 4)
        self.pg_texture.filter = moderngl.NEAREST, moderngl.NEAREST

        self.texture_program = self.load_program('programs/texture.glsl')
        self.quad_fs = geometry.quad_fs()

    def render(self, time, frametime):
        self.render_pygame(time)

        self.ctx.clear(
            (math.sin(time) + 1.0) / 2,
            (math.sin(time + 2) + 1.0) / 2,
            (math.sin(time + 3) + 1.0) / 2,
        )
    
        self.ctx.enable(moderngl.BLEND)
        self.pg_texture.use()
        self.quad_fs.render(self.texture_program)
        self.ctx.disable(moderngl.BLEND)

    def render_pygame(self, time):
        """Render to offscreen surface and copy result into moderngl texture"""
        self.pg_screen.fill((0, 0, 0, 0))  # Make sure we clear with alpha 0!
        N = 8
        for i in range(N):
            time_offset = 6.28 / N * i
            pygame.draw.circle(
                self.pg_screen,
                ((i * 50) % 255, (i * 100) % 255, (i * 20) % 255),
                (
                    math.sin(time + time_offset) * 55 + self.pg_res[0] // 2,
                    math.cos(time + time_offset) * 55 + self.pg_res[1] // 2),
                math.sin(time) * 4 + 15,
            )

        # Get the buffer view of the Surface's pixels
        # and write this data into the texture
        texture_data = self.pg_screen.get_view('1')
        self.pg_texture.write(texture_data)


if __name__ == '__main__':
    Pygame.run()
