from pathlib import Path

import moderngl
from pyrr import Matrix44
import moderngl_window


class FragmentPicking(moderngl_window.WindowConfig):
    title = "Fragment Picking"
    gl_version = 3, 3
    aspect_ratio = None
    resource_dir = (Path(__file__) / '../../resources').resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Object rotation
        self.x_rot = 0
        self.y_rot = 0

        self.scene = self.load_scene('scenes/fragment_picking/centered.obj')
        self.mesh = self.scene.root_nodes[0]

    def render(self, time, frametime):
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        projection = Matrix44.perspective_projection(60, self.wnd.aspect_ratio, 1, 100, dtype='f4')
        translation = Matrix44.from_translation((0, 0, -50))
        rotation = Matrix44.from_eulers((self.y_rot, self.x_rot, 0))
        modelview = translation * rotation

        self.scene.draw(
            projection,
            modelview,
        )

    def mouse_drag_event(self, x, y, dx, dy):
        self.x_rot -= dx / 100
        self.y_rot -= dy / 100


if __name__ == '__main__':
    moderngl_window.run_window_config(FragmentPicking)
