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
import glm

# from moderngl_window.conf import settings
# settings.SCREENSHOT_PATH = 'capture'
# from moderngl_window import screenshot


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

        if self.wnd.name != "pygame2":
            raise RuntimeError("This example only works with --window pygame2 option")

        self.pg_res = (160, 160)
        # Create a 24bit (rgba) offscreen surface pygame can render to
        self.pg_screen = pygame.Surface(self.pg_res, flags=pygame.SRCALPHA)
        # 24 bit (rgba) moderngl texture
        self.pg_texture = self.ctx.texture(self.pg_res, 4)
        self.pg_texture.filter = moderngl.NEAREST, moderngl.NEAREST
        self.pg_texture.swizzle = "BGRA"

        # Simple geometry and shader to render
        self.cube = geometry.cube(size=(2.0, 2.0, 2.0))
        self.texture_prog = self.load_program("programs/cube_simple_texture.glsl")
        self.texture_prog["m_proj"].write(
            glm.perspective(glm.radians(60), self.wnd.aspect_ratio, 1, 100)
        )
        self.texture_prog["m_model"].write(glm.mat4())

    def render(self, time, frametime):
        # time = self.wnd.frames / 30

        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.render_pygame(time)

        rotate = glm.mat4(glm.quat(glm.vec3(time, time * 1.2, time * 1.3)))
        translate = glm.translate(glm.vec3(0, 0, -3.5))
        camera = translate * rotate

        self.texture_prog["m_camera"].write(camera)
        self.pg_texture.use()
        self.cube.render(self.texture_prog)

        # screenshot.create(self.wnd.fbo, name='frame_{}.png'.format(str(self.wnd.frames).zfill(4)))

    def render_pygame(self, time):
        """Render to offscreen surface and copy result into moderngl texture"""
        self.pg_screen.fill((255, 255, 255))
        N = 8
        for i in range(N):
            time_offset = 6.28 / N * i
            pygame.draw.circle(
                self.pg_screen,
                ((i * 50) % 255, (i * 100) % 255, (i * 20) % 255),
                (
                    math.sin(time + time_offset) * 55 + self.pg_res[0] // 2,
                    math.cos(time + time_offset) * 55 + self.pg_res[1] // 2,
                ),
                math.sin(time) * 4 + 15,
            )

        # Get the buffer view of the Surface's pixels
        # and write this data into the texture
        texture_data = self.pg_screen.get_view("1")
        self.pg_texture.write(texture_data)


if __name__ == "__main__":
    moderngl_window.run_window_config(Pygame, args=("--window", "pygame2"))
