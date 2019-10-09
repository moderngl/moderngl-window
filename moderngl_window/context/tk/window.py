"""
Temp resource
    https://www.python-course.eu/tkinter_events_binds.php
"""
import time
import tkinter
import moderngl

from moderngl_window.context.base import BaseWindow
from pyopengltk import OpenGLFrame


class Window(BaseWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._tk = tkinter.Tk()
        self._gl_widget = ModernglTkWindow(self._tk, width=self.width, height=self.height)
        self._gl_widget.pack(fill=tkinter.BOTH, expand=tkinter.YES)

        # Configure is the tkinter's resize event
        self._gl_widget.bind('<Configure>', self.tk_resize)
        self._tk.protocol("WM_DELETE_WINDOW", self.tk_close_window)

        self._tk.title(self._title)

        # Ensure the window is opened/visible
        self._tk.update()

        self._gl_widget.tkMakeCurrent()
        self.init_mgl_context()
        self.set_default_viewport()

    def swap_buffers(self):
        """tkinter buffer swapping"""

        err = self._ctx.error
        if err != 'GL_NO_ERROR':
            print(err)

        # Ensure we process events or tkinter will eventually stall.
        self._tk.update_idletasks()
        self._tk.update()

        self._gl_widget.tkSwapBuffers()
        self._frames += 1

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

    def tk_close_window(self):
        """tkinter close window callback"""
        self._close = True

    def destroy(self):
        """Destroy logic for tkinter window. Currently empty."""
        pass


class ModernglTkWindow(OpenGLFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def redraw(self):
        """pyopengltk's own render method."""
        pass

    def initgl(self):
        """pyopengltk's user code for initialization."""
        pass

    def tkResize(self, event):
        """Should never be called. Event overidden."""
        raise ValueError("tkResize should never be called. The event is overriden.")

    def tkMap(self, event):
        """Called when frame goes onto the screen"""
        # Only create context once
        # In a window like this we are not likely to lose the context
        # even when window is minimized.
        if not getattr(self, '_wid', None):
            super().tkMap(event)
