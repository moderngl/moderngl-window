"""
Shadow mapping example from:
https://www.opengl-tutorial.org/intermediate-tutorials/tutorial-16-shadow-mapping/
"""
from pathlib import Path
import moderngl_window


class ShadowMapping(moderngl_window.WindowConfig):
    title = "Shadow Mapping"
    resource_dir = (Path(__file__) / '../../resources').resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.linearize_depth_program = self.load_program('programs/linearize_depth.glsl')

        # Offscreen buffer
        self.offscreen_depth = self.ctx.depth_texture(self.wnd.buffer_size)
        self.offscreen_color = self.ctx.texture(self.wnd.buffer_size, 4)
        self.offscreen = self.ctx.framebuffer(
            color_attachments=[self.offscreen_color],
            depth_attachment=self.offscreen_depth,
        )

    def render(self, time, frametime):
        pass


if __name__ == '__main__':
    moderngl_window.run_window_config(ShadowMapping)
