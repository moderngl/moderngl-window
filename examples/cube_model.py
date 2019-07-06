from pathlib import Path
from pyrr import Matrix44, matrix44, Vector3

import moderngl
import moderngl_window as mglw
from moderngl_window import resources
from moderngl_window.resources.meta import (
    SceneDescription,
    TextureDescription,
)

mglw.register_resource_dir(Path(__file__).parent / 'resources')


class CubeModel(mglw.WindowConfig):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cube = resources.scenes.load(SceneDescription(path='scenes/crate.obj', label='crate'))
        # self.texture = resources.textures.load(TextureDescription(path='textures/crate.png', label='crate'))

    def render(self, time, frametime):
        """Render the scene"""
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        proj = matrix44.create_perspective_projection(75, self.wnd.aspect_ratio, 0.1, 100)

        # Create camera matrix with rotation and translation
        translation = matrix44.create_from_translation((0, 0, -1.5))
        rotation = matrix44.create_from_eulers((time, time, time))
        camera = matrix44.multiply(rotation, translation)

        self.cube.draw(
            projection_matrix=proj,
            camera_matrix=camera,
            time=time,
        )


if __name__ == '__main__':
    mglw.run_window_config(CubeModel)
