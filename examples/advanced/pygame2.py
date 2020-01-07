"""
Based on BlubberQuark's blog:
https://blubberquark.tumblr.com/post/185013752945/using-moderngl-for-post-processing-shaders-with
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
    Needs to run with ``--window pygame`` option.
    """
    title = "Pygame"
    # window_size = 1280, 720
    window_size = 640, 360
    resource_dir = (Path(__file__) / '../../resources').absolute()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.wnd.name != 'pygame2':
            raise RuntimeError('This example only works with --window pygame2 option')

        self.pg_res = (256, 144)
        # Create a 24bit (rgb) offscreen surface pygame can render to
        self.pg_screen = pygame.Surface(self.pg_res).convert((255, 65280, 16711680, 0))
        # 24 bit (rgb) moderngl texture
        self.pg_texture = self.ctx.texture(self.pg_res, 3)
        self.pg_texture.filter = moderngl.NEAREST, moderngl.NEAREST

        # Simple geometry and shader to render
        self.quad_fs = geometry.quad_fs()
        self.texture_prog = self.load_program('programs/texture.glsl')

    def render(self, time, frametime):
        self.render_pygame(time)
        self.pg_texture.use()
        self.quad_fs.render(self.texture_prog)

    def render_pygame(self, time):
        """Render to offscreen surface and copy result into moderngl texture"""
        self.pg_screen.fill((50, 50, 50))
        # pygame.draw.line(self.pg_screen, (250, 250, 0), (0, 120), (160, 0))
        N = 8
        for i in range(N):
            time_offset = 6.28 / N * i
            pygame.draw.circle(
                self.pg_screen,
                (255, 255, 255),
                (
                    math.sin(time + time_offset) * 50 + self.pg_res[0] // 2,
                    math.cos(time + time_offset) * 50 + self.pg_res[1] // 2),
                math.sin(time) * 10 + 15,
            )

        # Get the buffer view of the Surface's pixels
        # and write this data into the texture
        texture_data = self.pg_screen.get_view('1')
        self.pg_texture.write(texture_data)


if __name__ == '__main__':
    Pygame.run()
