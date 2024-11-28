from pathlib import Path
from typing import Any, Optional

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

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._fbo: Optional[moderngl.Framebuffer] = None
        self._vsync = False  # We don't care about vsync in headless mode
        self._resizable = False  # headless window is not resizable
        self._cursor = False  # Headless don't have a cursor
        self._headless = True
        self.init_mgl_context()
        self.set_default_viewport()

    @property
    def fbo(self) -> moderngl.Framebuffer:
        """moderngl.Framebuffer: The default framebuffer"""
        assert self._fbo is not None, "No default framebuffer defined"
        return self._fbo

    def init_mgl_context(self) -> None:
        """Create an standalone context and framebuffer"""
        if self._backend is not None:
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

    def _create_fbo(self) -> None:
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
    def size(self, value: tuple[int, int]) -> None:
        if value == (self._width, self._height):
            return
        self._width, self._height = value
        self._create_fbo()

    def use(self) -> None:
        """Bind the window's framebuffer"""
        assert self._fbo is not None, "No framebuffer defined, did you forget to call create_fbo()?"
        self._fbo.use()

    def clear(
        self,
        red: float = 0.0,
        green: float = 0.0,
        blue: float = 0.0,
        alpha: float = 0.0,
        depth: float = 1.0,
        viewport: Optional[tuple[int, int, int, int]] = None,
    ) -> None:
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

    def _set_icon(self, icon_path: Path) -> None:
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
