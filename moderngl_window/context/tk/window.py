import time
import tkinter
import moderngl

from moderngl_window.context.base import BaseWindow
from pyopengltk import OpenGLFrame


class Window(BaseWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.root = tkinter.Tk()
        self.gl_widget = ModernglTkWindow(self.root, width=self.width, height=self.height)
        self.gl_widget.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.gl_widget.bind('<Configure>', self.tk_resize)

        self.gl_widget.winfo_toplevel().title(self._title)

        # Ensure the window is opened/visible
        self.root.update()

        self.gl_widget.tkMakeCurrent()
        self.init_mgl_context()
        self.set_default_viewport()

    def swap_buffers(self):
        """tkinter buffer swapping"""

        err = self._ctx.error
        if err != 'GL_NO_ERROR':
            print(err)

        # Ensure we process events or tkinter will eventually stall.
        self.root.update_idletasks()
        self.root.update()

        self.gl_widget.tkSwapBuffers()

    def tk_resize(self, event):
        """tkinter specific window resize event.
        Forwards resize events to the configured resize function.

        Args:
            event (tkinter.Event): The resize event
        """
        self._width, self._height = event.width, event.height
        # TODO: How do we know the actual buffer size?
        self._buffer_width, self._buffer_height = event.width, event.height
        self.set_default_viewport()
        self._resize_func(event.width, event.height)


class ModernglTkWindow(OpenGLFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def redraw(self):
        """pyopengltk's own render method."""
        print("ModernglTkWindow.redraw", time.time())

    def initgl(self):
        print("ModernglTkWindow.initgl", time.time())
        pass

    def tkResize(self, event):
        """Should never be called. Event overidden."""
        pass

    def tkMap(self, event):
        """Called when frame goes onto the screen"""
        print("ModernglTkWindow.tkMap", time.time())
        super().tkMap(event)
