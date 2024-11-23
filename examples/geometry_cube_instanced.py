"""
Renders 100 x 100 cubes using instancing.
We are using the moderngl-window specific VAO wrapper.

Each cube is animated in the vertex shader offset by gl_InstanceID
"""

from pathlib import Path

import numpy
import glm
import moderngl
import moderngl_window
from moderngl_window import geometry
from base import CameraWindow


class CubeSimpleInstanced(CameraWindow):
    """Renders cubes using instancing"""

    title = "Plain Cube"
    resource_dir = (Path(__file__).parent / "resources").resolve()
    aspect_ratio = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.camera.projection.update(near=1, far=1000)
        self.cube = geometry.cube(size=(2, 2, 2))
        self.prog = self.load_program("programs/cube_simple_instanced.glsl")
        self.prog["m_model"].write(glm.mat4())

        # Generate per instance data represeting a grid of cubes
        N = 100
        self.instances = N * N

        def gen_data(x_res, z_res, spacing=2.5):
            """Generates a grid of N * N position and random colors on the xz plane"""
            for y in range(z_res):
                for x in range(x_res):
                    yield -N * spacing / 2 + spacing * x
                    yield 0
                    yield -N * spacing / 2 + spacing * y
                    yield numpy.random.uniform(0, 1)
                    yield numpy.random.uniform(0, 1)
                    yield numpy.random.uniform(0, 1)

        self.instance_data = self.ctx.buffer(
            numpy.fromiter(gen_data(N, N), "f4", count=self.instances * 6)
        )
        self.cube.buffer(self.instance_data, "3f 3f/i", ["in_offset", "in_color"])

    def render(self, time: float, frametime: float) -> None:
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        self.prog["m_proj"].write(self.camera.projection.matrix)
        self.prog["m_camera"].write(self.camera.matrix)
        self.prog["time"].value = time

        self.cube.render(self.prog, instances=self.instances)


if __name__ == "__main__":
    moderngl_window.run_window_config(CubeSimpleInstanced)
