"""
Based on BlubberQuark's blog:
https://blubberquark.tumblr.com/post/185013752945/using-moderngl-for-post-processing-shaders-with

Clears the screen using opengl with a constantly changing
color value and alpha blend a pygame surface on top.
"""

import math
from pathlib import Path

import moderngl
import pygame

import moderngl_window
from moderngl_window import geometry


class Pygame(moderngl_window.WindowConfig):
    """
    Example using pygame with moderngl.
    Needs to run with ``--window pygame2`` option.
    """

    title = "Pygame"
    window_size = 1280, 720
    resource_dir = (Path(__file__) / "../../resources").absolute()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a 24bit (rgba) offscreen surface pygame can render to
        self.pg_screen = pygame.Surface(self.window_size, flags=pygame.SRCALPHA)
        # 24 bit (rgba) moderngl texture
        self.pg_texture = self.ctx.texture(self.window_size, 4)
        self.pg_texture.filter = moderngl.NEAREST, moderngl.NEAREST
        self.pg_texture.swizzle = "BGRA"

        self.texture_program = self.load_program("programs/texture.glsl")
        self.quad_texture = self.load_texture_2d("textures/python-bg.png")
        self.quad_fs = geometry.quad_fs()

    def on_render(self, time: float, frametime: float):
        self.ctx.clear()

        self.ctx.enable(moderngl.BLEND)

        # Render background graphics
        self.quad_texture.use()
        self.texture_program["texture0"].value = 0
        self.quad_fs.render(self.texture_program)

        # Render foreground objects
        self.pg_texture.use()
        self.render_pygame(time)
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
                    math.sin(time + time_offset) * 200 + self.window_size[0] // 2,
                    math.cos(time + time_offset) * 200 + self.window_size[1] // 2,
                ),
                math.sin(time) * 7 + 15,
            )

        # Get the buffer view of the Surface's pixels
        # and write this data into the texture
        texture_data = self.pg_screen.get_view("1")
        self.pg_texture.write(texture_data)


if __name__ == "__main__":
    moderngl_window.run_window_config(Pygame, args=("--window", "pygame2"))
