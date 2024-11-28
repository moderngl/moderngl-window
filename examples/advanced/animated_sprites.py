from pathlib import Path

import glm
import moderngl

import moderngl_window as mglw
from moderngl_window import geometry

# from moderngl_window.conf import settings
# settings.SCREENSHOT_PATH = 'screenshots'
# from moderngl_window import screenshot


class Test(mglw.WindowConfig):
    title = "Animated Sprite"
    resource_dir = (Path(__file__) / "../../resources").resolve()
    aspect_ratio = 320 / 256
    window_size = 320 * 3, 256 * 3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buffer_size = 320, 256
        # Textures
        self.background_texture = self.load_texture_array(
            "textures/animated_sprites/giphy.gif"
        )
        self.background_texture.repeat_x = False
        self.background_texture.repeat_y = False
        self.caveman_texture = self.load_texture_array(
            "textures/animated_sprites/player_2.gif", layers=35
        )
        self.caveman_texture.repeat_x = False
        self.caveman_texture.repeat_y = False
        self.caveman_texture.filter = moderngl.NEAREST, moderngl.NEAREST

        # Geometry
        # One pixel quad 0, 0 -> 1.0, 1.0
        self.sprite_geometry = geometry.quad_2d(size=(1.0, 1.0), pos=(0.5, 0.5))
        self.quad_fs = geometry.quad_fs()

        # Programs
        self.sprite_program = self.load_program(
            "programs/animated_sprites/sprite_array.glsl"
        )
        self.texture_program = self.load_program("programs/texture.glsl")

        # Offscreen buffer
        self.offscreen_texture = self.ctx.texture(self.buffer_size, 4)
        self.offscreen_texture.filter = moderngl.NEAREST, moderngl.NEAREST
        self.offscreen = self.ctx.framebuffer(
            color_attachments=[self.offscreen_texture]
        )

        self.projection = glm.ortho(0, 320, 0, 256, -1.0, 1.0)
        self.sprite_program["projection"].write(self.projection)

    def render(self, time, frame_time):
        # Render sprite of offscreen
        self.offscreen.use()
        self.ctx.clear(0.5, 0.5, 0.5, 0.0)

        self.render_sprite(
            self.background_texture,
            frame=int(time * 15) % self.background_texture.layers,
        )
        self.render_sprite(
            self.caveman_texture,
            frame=int(time * 15) % self.caveman_texture.layers,
            blend=True,
            position=(260, 20),
        )

        # Display offscreen
        self.ctx.screen.use()
        self.offscreen_texture.use(location=0)
        self.quad_fs.render(self.texture_program)

        # if self.wnd.frames < 100:
        #     screenshot.create(self.ctx.screen)

    def render_sprite(self, texture, blend=False, frame=0, position=(0, 0)):
        if blend:
            self.ctx.enable(moderngl.BLEND)

        texture.use(location=0)
        self.sprite_program["layer_id"] = frame
        self.sprite_program["position"] = position
        self.sprite_geometry.render(self.sprite_program)

        if blend:
            self.ctx.disable(moderngl.BLEND)


if __name__ == "__main__":
    mglw.run_window_config(Test)
    # Test.run()
