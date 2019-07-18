import moderngl

from moderngl_window.context.base import BaseWindow
from moderngl_window.context.headless.keys import Keys


class Window(BaseWindow):
    """Headless window.

    Do not currently support any form window events or key input.
    """
    keys = Keys

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._fbo = None
        self.init_mgl_context()

    @property
    def fbo(self) -> moderngl.Framebuffer:
        """moderngl.Framebuffer: The default framebuffer"""
        return self._ctx.screen

    def init_mgl_context(self) -> None:
        """Create an standalone context and framebuffer"""
        self._ctx = moderngl.create_standalone_context(require=self.gl_version_code)
        self._fbo = self.ctx.framebuffer(
            color_attachments=self.ctx.texture(self.size, 4),
            depth_attachment=self.ctx.depth_texture(self.size),
        )

    def use(self):
        """Bind the window's framebuffer"""
        self._fbo.use()

    def clear(self, red=0.0, green=0.0, blue=0.0, alpha=0.0, depth=1.0, viewport=None):
        """
        Clear the default framebuffer

        Args:
            red (float): color component
            green (float): color component
            blue (float): color component
            alpha (float): alpha component
            depth (float): depth value
            viewport (tuple): The viewport
        """
        self._fbo.clear(red=red, green=green, blue=blue, alpha=alpha, depth=depth, viewport=viewport)

    def swap_buffers(self) -> None:
        """
        Placeholder. We currently don't do double buffering in headless mode.
        This may change in the future.
        """
        # TODO: No double buffering currently

    def destroy(self) -> None:
        # TODO: A context can currently not be invaldiated in ModernGL
