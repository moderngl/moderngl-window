import moderngl
from pathlib import Path
import moderngl_window as mglw
from moderngl_window import geometry
from pyrr import Matrix44


class Test(mglw.WindowConfig):
    resource_dir = (Path(__file__) / '../../resources').resolve()
    aspect_ratio = 320 / 256

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buffer_size = 320, 256
        # Textures
        self.sprite_texture = self.load_texture_array('textures/animated_sprites/player_2.png', layers=35)
        self.sprite_texture.repeat_x = False
        self.sprite_texture.repeat_y = False
        self.sprite_texture.filter = moderngl.NEAREST, moderngl.NEAREST

        # Geometry
        self.sprite_geometry = geometry.quad_2d()
        self.quad_fs = geometry.quad_fs()

        # Programs
        self.sprite_program = self.load_program('programs/animated_sprites/sprite_array.glsl')
        self.texture_program = self.load_program('programs/texture.glsl')

        # Offscreen buffer
        self.offscreen_texture = self.ctx.texture(self.buffer_size, 4)
        self.offscreen_texture.filter = moderngl.NEAREST, moderngl.NEAREST
        self.offscreen = self.ctx.framebuffer(color_attachments=[self.offscreen_texture])

        self.projection = Matrix44.orthogonal_projection(0, 320, 0, 256, -1.0, 1.0, dtype='f4')

    def render(self, time, frame_time):
        # Render sprite of offscreen
        self.offscreen.use()
        self.ctx.clear(1.0, 1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.BLEND)

        self.sprite_texture.use(location=0)
        self.sprite_program['projection'].write(self.projection)
        self.sprite_program['layer_id'] = int(time * 10) % 35
        self.sprite_program['size'] = self.sprite_texture.width, self.sprite_texture.height
        self.sprite_program['position'] = 150, 120
        self.sprite_geometry.render(self.sprite_program)

        # Display offscreen
        self.ctx.screen.use()
        self.offscreen_texture.use(location=0)
        self.quad_fs.render(self.texture_program)


if __name__ == '__main__':
    Test.run()
