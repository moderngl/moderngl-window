"""
6 cubes with drag and drop texture loading.

For each box, locate an image in your File Manager, and drag and drop onto the box.

Currently only working with the Pyglet backend.
"""
from pathlib import Path
import os

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
        self.box_top_left = self.load_scene('scenes/box/box-T2F_V3F.obj')
        self.box_top_middle = self.load_scene('scenes/box/box-T2F_V3F.obj')
        self.box_top_right = self.load_scene('scenes/box/box-T2F_V3F.obj')
        self.box_bottom_left = self.load_scene('scenes/box/box-T2F_V3F.obj')
        self.box_bottom_middle = self.load_scene('scenes/box/box-T2F_V3F.obj')
        self.box_bottom_right = self.load_scene('scenes/box/box-T2F_V3F.obj')

        self.resize(*self.wnd.size)

    def render(self, time, frame_time):
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        rot = Matrix44.from_eulers((time, time/2, time/3))

        # Box top left
        view = Matrix44.from_translation((-5, 2, -10), dtype='f4')
        self.box_top_left.draw(self.projection, view * rot)

        # Box top middle
        view = Matrix44.from_translation((0, 2, -10), dtype='f4')
        self.box_top_middle.draw(self.projection, view * rot)

        # Box top right
        view = Matrix44.from_translation((5, 2, -10), dtype='f4')
        self.box_top_right.draw(self.projection, view * rot)

        # Box bottom left
        view = Matrix44.from_translation((-5, -2, -10), dtype='f4')
        self.box_bottom_left.draw(self.projection, view * rot)

        # Box bottom middle
        view = Matrix44.from_translation((0, -2, -10), dtype='f4')
        self.box_bottom_middle.draw(self.projection, view * rot)

        # Box bottom right
        view = Matrix44.from_translation((5, -2, -10), dtype='f4')
        self.box_bottom_right.draw(self.projection, view * rot)

    def resize(self, width, height):
        self.ctx.viewport = 0, 0, width, height
        self.projection = Matrix44.perspective_projection(45, width / height, 1, 50, dtype='f4')

    def _load_texture(self, path):
        tex = self.load_texture_2d(os.path.relpath(path, self.resource_dir))
        print(type(tex))
        return tex

    def files_dropped_event(self, x, y, paths):
        if x < self.wnd._window.width * 0.33:
            if y < self.wnd._window.height * 0.5:
                # Modify top left box
                self.box_top_left.materials[0].mat_texture.texture = \
                    self._load_texture(paths[0])
            else:
                # Modify bottom left box
                self.box_bottom_left.materials[0].mat_texture.texture = \
                    self._load_texture(paths[0])
        elif x < self.wnd._window.width * 0.66:
            if y < self.wnd._window.height * 0.5:
                # Modify top middle box
                self.box_top_middle.materials[0].mat_texture.texture = \
                    self._load_texture(paths[0])
            else:
                # Modify bottom middle box
                self.box_bottom_middle.materials[0].mat_texture.texture = \
                    self._load_texture(paths[0])
        else:
            if y < self.wnd._window.height * 0.5:
                # Modify top right box
                self.box_top_right.materials[0].mat_texture.texture = \
                    self._load_texture(paths[0])
            else:
                # Modify bottom right box
                self.box_bottom_right.materials[0].mat_texture.texture = \
                    self._load_texture(paths[0])
        print(paths)

if __name__ == '__main__':
    Cubes.run()
