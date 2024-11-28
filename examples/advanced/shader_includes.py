"""
Example showing the use of #include in shaders.
This can be used to include reusable library functions.

We include a library doing different blend types
and render each quadrant of the screen with different blend types
"""
from pathlib import Path

import moderngl_window as mglw
from moderngl_window import geometry


class ShaderInclude(mglw.WindowConfig):
    title = "Shader Include"
    resource_dir = (Path(__file__) / '../../resources').resolve()
    aspect_ratio = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.program = self.load_program('programs/blend_include.glsl')
        self.texture_0 = self.load_texture_2d('textures/cubemaps/yokohama/negx.jpg')
        self.texture_1 = self.load_texture_2d('textures/cubemaps/yokohama/negz.jpg')
        self.quad_fs = geometry.quad_fs()

    def render(self, time, frame_time):
        self.texture_0.use(location=0)
        self.texture_1.use(location=1)
        self.quad_fs.render(self.program)


if __name__ == '__main__':
    mglw.run_window_config(ShaderInclude)
