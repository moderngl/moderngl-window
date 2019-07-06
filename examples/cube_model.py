from pathlib import Path
from pyrr import Matrix44, matrix44, Vector3

import moderngl
import moderngl_window as mglw
from moderngl_window import resources
from moderngl_window.resources.meta import SceneDescription

from moderngl_window.conf import settings

mglw.register_resource_dir(Path(__file__).parent / 'resources')


class CubeModel(mglw.WindowConfig):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cube = resources.scenes.load(SceneDescription(path='scenes/crate.obj', label='crate'))

    def render(self, time, frametime):
        pass


if __name__ == '__main__':
    mglw.run_window_config(CubeModel)
