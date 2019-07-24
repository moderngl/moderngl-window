from PyQt5 import QtCore, QtOpenGL, QtWidgets

from moderngl_window.context.base import BaseWindow
from moderngl_window.context.pyqt5.keys import Keys


class Window(BaseWindow):
    """
    A basic window implementation using PyQt5 with the goal of
    creating an OpenGL context and handle keyboard and mouse input.

    This window bypasses Qt's own event loop to make things as flexible as possible.

    If you need to use the event loop and are using other features
    in Qt as well, this example can still be useful as a reference
    when creating your own window.
    """
    keys = Keys

    # PyQt supports mode buttons, but we are limited by other libraries
    _mouse_button_map = {
        1: 1,
        2: 2,
        4: 3,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Specify OpenGL context parameters
        gl = QtOpenGL.QGLFormat()
        gl.setVersion(self.gl_version[0], self.gl_version[1])
        gl.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        gl.setDepthBufferSize(24)
        gl.setDoubleBuffer(True)
        gl.setSwapInterval(1 if self.vsync else 0)

        # Configure multisampling if needed
        if self.samples > 1:
            gl.setSampleBuffers(True)
            gl.setSamples(self.samples)

        # We need an application object, but we are bypassing the library's
        # internal event loop to avoid unnecessary work
        self.app = QtWidgets.QApplication([])

        # Create the OpenGL widget
        self.widget = QtOpenGL.QGLWidget(gl)
        self.widget.setWindowTitle(self.title)

        # If fullscreen we change the window to match the desktop on the primary screen
        if self.fullscreen:
            rect = QtWidgets.QDesktopWidget().screenGeometry()
            self._width = rect.width()
            self._height = rect.height()
            self._buffer_width = rect.width() * self.widget.devicePixelRatio()
            self._buffer_height = rect.height() * self.widget.devicePixelRatio()

        if self.resizable:
            # Ensure a valid resize policy when window is resizable
            size_policy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding,
            )
            self.widget.setSizePolicy(size_policy)
            self.widget.resize(self.width, self.height)
        else:
            self.widget.setFixedSize(self.width, self.height)

        # Center the window on the screen if in window mode
        if not self.fullscreen:
            self.widget.move(QtWidgets.QDesktopWidget().rect().center() - self.widget.rect().center())

        # Needs to be set before show()
        self.widget.resizeGL = self.resize

        if not self.cursor:
            self.widget.setCursor(QtCore.Qt.BlankCursor)

        if self.fullscreen:
            self.widget.showFullScreen()
        else:
            self.widget.show()

        # We want mouse position events
        self.widget.setMouseTracking(True)

        # Override event functions in qt
        self.widget.keyPressEvent = self.key_pressed_event
        self.widget.keyReleaseEvent = self.key_release_event
        self.widget.mouseMoveEvent = self.mouse_move_event
        self.widget.mousePressEvent = self.mouse_press_event
        self.widget.mouseReleaseEvent = self.mouse_release_event
        self.widget.closeEvent = self.close_event

        # Attach to the context
        self.init_mgl_context()

        # Ensure retina and 4k displays get the right viewport
        self._buffer_width = self._width * self.widget.devicePixelRatio()
        self._buffer_height = self._height * self.widget.devicePixelRatio()

        self.set_default_viewport()

    def swap_buffers(self):
        """
        Swap buffers, set viewport, trigger events and increment frame counter
        """
        self.widget.swapBuffers()
        self.set_default_viewport()
        self.app.processEvents()
        self._frames += 1

    def resize(self, width: int, height: int):
        """
        Replacement for Qt's resizeGL method.
        """
        self._width = width // self.widget.devicePixelRatio()
        self._height = height // self.widget.devicePixelRatio()
        self._buffer_width = width
        self._buffer_height = height

        if self._ctx:
            self.set_default_viewport()

        # Make sure we notify the example about the resize
        super().resize(self._buffer_width, self._buffer_height)

    def _handle_modifiers(self, mods):
        self._modifiers.shift = mods & QtCore.Qt.ShiftModifier
        self._modifiers.ctrl = mods & QtCore.Qt.ControlModifier

    def key_pressed_event(self, event):
        """
        Process Qt key press events forwarding them to the example
        """
        if event.key() == self.keys.ESCAPE:
            self.close()

        self._handle_modifiers(event.modifiers())
        self._key_pressed_map[event.key()] = True
        self.key_event_func(event.key(), self.keys.ACTION_PRESS, self._modifiers)

    def key_release_event(self, event):
        """
        Process Qt key release events forwarding them to the example
        """
        self._handle_modifiers(event.modifiers())
        self._key_pressed_map[event.key()] = False
        self.key_event_func(event.key(), self.keys.ACTION_RELEASE, self._modifiers)

    def mouse_move_event(self, event):
        """
        Forward mouse cursor position events to the example
        """
        self.mouse_position_event_func(event.x(), event.y())

    def mouse_press_event(self, event):
        """
        Forward mouse press events to the example
        """
        button = self._mouse_button_map.get(event.button())
        if button is None:
            return

        self.mouse_press_event_func(event.x(), event.y(), button)

    def mouse_release_event(self, event):
        """
        Forward mouse release events to the example
        """
        button = self._mouse_button_map.get(event.button())
        if button is None:
            return

        self.mouse_release_event_func(event.x(), event.y(), button)

    def close_event(self, event):
        """
        Detect the standard PyQt close events to make users happy
        """
        self.close()

    def destroy(self):
        """
        Quit the Qt application to exit the window gracefully
        """
        QtCore.QCoreApplication.instance().quit()
