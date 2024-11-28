from pathlib import Path

import glm
import moderngl
import numpy
from base import CameraWindow

import moderngl_window


class LinesDemo(CameraWindow):
    """Rendering thick lines with geometry shader

    Example is basic and incomplete, but shows how
    one could use the geometry shader to create simple thick lines.
    """

    gl_version = (3, 3)
    title = "Thick Lines"
    resource_dir = (Path(__file__) / "../resources").absolute()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True

        self.prog = self.load_program("programs/lines/lines.glsl")
        self.prog["color"].value = (1.0, 1.0, 1.0, 1.0)
        self.prog["m_model"].write(glm.translate(glm.vec3(0.0, 0.0, -3.5)))

        N = 10

        # Create lines geometry
        def gen_lines():
            for i in range(N):
                # A
                yield -1.0
                yield 1.0 - i * 2.0 / N
                yield 0.0
                # b
                yield 1.0
                yield 1.0 - i * 2.0 / N
                yield 0.0

        buffer = self.ctx.buffer(numpy.fromiter(gen_lines(), dtype="f4", count=N * 6).tobytes())
        self.lines = self.ctx.vertex_array(
            self.prog,
            [
                (buffer, "3f", "in_position"),
            ],
        )

    def on_render(self, time: float, frametime: float):
        # self.ctx.enable_only(moderngl.DEPTH_TEST)

        self.prog["m_proj"].write(self.camera.projection.matrix)
        self.prog["m_cam"].write(self.camera.matrix)
        self.lines.render(mode=moderngl.LINES)


if __name__ == "__main__":
    moderngl_window.run_window_config(LinesDemo)
