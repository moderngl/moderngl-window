import numpy as np
from PIL import Image
import moderngl
import moderngl_window


class HeadlessTest(moderngl_window.WindowConfig):
    """
    Simple one frame renderer writing to png and exit.
    If you need more fancy stuff, see the custom_config* examples.
    """

    samples = 0  # Headless is not always happy with multisampling

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.wnd.name != "headless":
            raise RuntimeError("This example only works with --window headless option")

        prog = self.ctx.program(
            vertex_shader="""
            #version 330

            in vec2 in_vert;
            in vec3 in_color;
            out vec3 color;

            void main() {
                gl_Position = vec4(in_vert, 0.0, 1.0);
                color = in_color;
            }
            """,
            fragment_shader="""
            #version 330

            out vec4 fragColor;
            in vec3 color;

            void main() {
                fragColor = vec4(color, 1.0);
            }
            """,
        )
        # fmt: off
        vertices = np.array([
            -1.0,  -1.0,   1.0, 0.0, 0.0,
            1.0,  -1.0,   0.0, 1.0, 0.0,
            0.0,   1.0,   0.0, 0.0, 1.0],
            dtype='f4',
        )
        # fmt: on
        self.vao = self.ctx.simple_vertex_array(
            prog, self.ctx.buffer(vertices), "in_vert", "in_color"
        )

    def render(self, time, frame_time):
        """Render one frame, save to png and close it"""
        # Fill currently bound framebuffer with while background
        self.ctx.clear(1, 1, 1, 1)
        # Render the geometry
        self.vao.render(mode=moderngl.TRIANGLES)

        # Wait for all rendering calls to finish (Might not be needed)
        self.ctx.finish()

        image = Image.frombytes("RGBA", self.wnd.fbo.size, self.wnd.fbo.read(components=4))
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save("triangle.png", format="png")

        self.wnd.close()


if __name__ == "__main__":
    HeadlessTest.run()
