from pathlib import Path
import glm

import moderngl

import moderngl_window
from moderngl_window import geometry
from base import CameraWindow


class TextureArrayExample(CameraWindow):
    """
    Cycles different texture layers in an array texture
    rendered on a cube.
    """
    title = "Texture Array"
    resource_dir = (Path(__file__).parent / 'resources').resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.num_layers = 10
        self.cube = geometry.cube(size=(2, 2, 2))
        self.texture = self.load_texture_array(
            'textures/array.png', layers=self.num_layers, mipmap=True, anisotrpy=8.0)
        self.prog = self.load_program('programs/cube_texture_array.glsl')
        self.prog['texture0'].value = 0
        self.prog['num_layers'].value = 10

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        rotation = glm.mat4(glm.quat(glm.vec3(time, time, time)))
        translation = glm.translate(glm.vec3(0.0, 0.0, -3.5))
        modelview = translation * rotation

        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_model'].write(modelview)
        self.prog['m_camera'].write(self.camera.matrix)
        self.prog['time'].value = time

        self.texture.use(location=0)
        self.cube.render(self.prog)


if __name__ == '__main__':
    moderngl_window.run_window_config(TextureArrayExample)
