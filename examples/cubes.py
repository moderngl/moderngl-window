"""
Cubes of different vertex formats.
These formats are unique for wavefront obj files.
"""
from pathlib import Path

import moderngl
import moderngl_window

from pyrr import Matrix44


class Cubes(moderngl_window.WindowConfig):
    title = "Cubes"
    resizable = True
    aspect_ratio = None
    resource_dir = Path(__file__).parent.resolve() / 'resources'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load the 6 different boxes with different vertex formats
        self.box_v3 = self.load_scene('scenes/box/box-V3F.obj')
        self.box_c3_v3 = self.load_scene('scenes/box/box-C3F_V3F.obj')
        self.box_n3_v3 = self.load_scene('scenes/box/box-N3F_V3F.obj')
        self.box_t2_v3 = self.load_scene('scenes/box/box-T2F_V3F.obj')
        self.box_t2_c3_v3 = self.load_scene('scenes/box/box-T2F_C3F_V3F.obj')
        self.box_t2_n3_v3 = self.load_scene('scenes/box/box-T2F_N3F_V3F.obj')

        self.resize(*self.wnd.size)

    def render(self, time, frame_time):
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        rot = Matrix44.from_eulers((time, time/2, time/3))

        # Box 1
        view = Matrix44.from_translation((-5, 2, -10), dtype='f4')
        self.box_v3.draw(self.projection, view * rot)

        # Box 2
        view = Matrix44.from_translation((0, 2, -10), dtype='f4')        
        self.box_c3_v3.draw(self.projection, view * rot)

        # Box 3
        view = Matrix44.from_translation((5, 2, -10), dtype='f4')
        self.box_n3_v3.draw(self.projection, view * rot)

        # Box 4
        view = Matrix44.from_translation((-5, -2, -10), dtype='f4')
        self.box_t2_v3.draw(self.projection, view * rot)

        # Box 5
        view = Matrix44.from_translation((0, -2, -10), dtype='f4')
        self.box_t2_c3_v3.draw(self.projection, view * rot)

        # Box 6
        view = Matrix44.from_translation((5, -2, -10), dtype='f4')
        self.box_t2_n3_v3.draw(self.projection, view * rot)

    def resize(self, width, height):
        self.ctx.viewport = 0, 0, width, height
        self.projection = Matrix44.perspective_projection(45, width / height, 1, 50, dtype='f4')


if __name__ == '__main__':
    Cubes.run()
