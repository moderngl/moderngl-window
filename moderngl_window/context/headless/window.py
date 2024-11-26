import moderngl
from moderngl_window.context.base import BaseWindow
from moderngl_window.context.headless.keys import Keys


class Window(BaseWindow):
    """Headless window.

    Do not currently support any form window events or key input.
    """

    #: Name of the window
    name = "headless"
    keys = Keys

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._fbo = None
        self._vsync = False  # We don't care about vsync in headless mode
        self._resizable = False  # headless window is not resizable
        self._cursor = False  # Headless don't have a cursor
        self._headless = True
        self.init_mgl_context()
        self.set_default_viewport()

    @property
    def fbo(self) -> moderngl.Framebuffer:
        """moderngl.Framebuffer: The default framebuffer"""
        return self._fbo

    def init_mgl_context(self) -> None:
        """Create an standalone context and framebuffer"""
        if self._backend:
            self._ctx = moderngl.create_standalone_context(
                require=self.gl_version_code,
                backend=self._backend,
            )
        else:
            self._ctx = moderngl.create_standalone_context(
                require=self.gl_version_code,
            )

        self._create_fbo()
        self.use()

    def _create_fbo(self):
        if self._fbo:
            for attachment in self._fbo.color_attachments:
                attachment.release()
            if self._fbo.depth_attachment:
                self._fbo.depth_attachment.release()
            self._fbo.release()

        self._fbo = self.ctx.framebuffer(
            color_attachments=self.ctx.texture(self.size, 4, samples=self._samples),
            depth_attachment=self.ctx.depth_texture(self.size, samples=self._samples),
        )

    @property
    def size(self) -> tuple[int, int]:
        """tuple[int, int]: current window size.

        This property also support assignment::

            # Resize the window to 1000 x 1000
            window.size = 1000, 1000
        """
        return self._width, self._height

    @size.setter
    def size(self, value: tuple[int, int]):
        if value == (self._width, self._height):
            return
        self._width, self._height = value
        self._create_fbo()

    def use(self):
        """Bind the window's framebuffer"""
        self._fbo.use()

    def clear(self, red=0.0, green=0.0, blue=0.0, alpha=0.0, depth=1.0, viewport=None):
        """
        Binds and clears the default framebuffer

        Args:
            red (float): color component
            green (float): color component
            blue (float): color component
            alpha (float): alpha component
            depth (float): depth value
            viewport (tuple): The viewport
        """
        self.use()
        self._ctx.clear(
            red=red, green=green, blue=blue, alpha=alpha, depth=depth, viewport=viewport
        )

    def swap_buffers(self) -> None:
        """
        Placeholder. We currently don't do double buffering in headless mode.
        This may change in the future.
        """
        # NOTE: No double buffering currently
        self._frames += 1
        self._ctx.finish()

    def _set_icon(self, icon_path: str) -> None:
        """Do nothing when icon is set"""
        pass

    def _set_fullscreen(self, value: bool) -> None:
        """Do nothing when fullscreen is toggled"""
        pass

    def _set_vsync(self, value: bool) -> None:
        pass

    def destroy(self) -> None:
        """Destroy the context"""
        self._ctx.release()
