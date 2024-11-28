"""
Cubes of different vertex formats.
These formats are unique for wavefront obj files.
"""

from pathlib import Path

import glm
import moderngl

import moderngl_window


class Cubes(moderngl_window.WindowConfig):
    title = "Cubes"
    resizable = True
    aspect_ratio = 16 / 9
    resource_dir = Path(__file__).parent.resolve() / "resources"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load the 6 different boxes with different vertex formats
        self.box_v3 = self.load_scene("scenes/box/box-V3F.obj")
        self.box_c3_v3 = self.load_scene("scenes/box/box-C3F_V3F.obj")
        self.box_n3_v3 = self.load_scene("scenes/box/box-N3F_V3F.obj")
        self.box_t2_v3 = self.load_scene("scenes/box/box-T2F_V3F.obj")
        self.box_t2_c3_v3 = self.load_scene("scenes/box/box-T2F_C3F_V3F.obj")
        self.box_t2_n3_v3 = self.load_scene("scenes/box/box-T2F_N3F_V3F.obj")

        self.on_resize(*self.wnd.size)

    def on_render(self, time, frame_time):
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        rot = glm.mat4(glm.quat(glm.vec3(time, time / 2, time / 3)))

        # Box 1
        view = glm.translate(glm.vec3(-5, 2, -10))
        self.box_v3.draw(self.projection, view * rot)

        # Box 2
        view = glm.translate(glm.vec3(0, 2, -10))
        self.box_c3_v3.draw(self.projection, view * rot)

        # Box 3
        view = glm.translate(glm.vec3(5, 2, -10))
        self.box_n3_v3.draw(self.projection, view * rot)

        # Box 4
        view = glm.translate(glm.vec3(-5, -2, -10))
        self.box_t2_v3.draw(self.projection, view * rot)

        # Box 5
        view = glm.translate(glm.vec3(0, -2, -10))
        self.box_t2_c3_v3.draw(self.projection, view * rot)

        # Box 6
        view = glm.translate(glm.vec3(5, -2, -10))
        self.box_t2_n3_v3.draw(self.projection, view * rot)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.projection = glm.perspective(glm.radians(45), self.aspect_ratio, 1, 50)


if __name__ == "__main__":
    Cubes.run()
