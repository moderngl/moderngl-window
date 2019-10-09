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

        self.gl_widget.winfo_toplevel().title(self._title)

        # Ensure the window is opened/visible
        self.root.update()

        self.gl_widget.tkMakeCurrent()
        self.init_mgl_context()

    def swap_buffers(self):
        self.root.update_idletasks()
        self.root.update()

        self.gl_widget.tkSwapBuffers()


class ModernglTkWindow(OpenGLFrame):

    def redraw(self):
        pass

    def initgl(self):
        pass
