from typing import Tuple
from PySide2 import QtCore, QtOpenGL, QtWidgets, QtGui

from moderngl_window.context.base import BaseWindow
from moderngl_window.context.pyside2.keys import Keys


class Window(BaseWindow):
    """
    A basic window implementation using PySide2 with the goal of
    creating an OpenGL context and handle keyboard and mouse input.

    This window bypasses Qt's own event loop to make things as flexible as possible.

    If you need to use the event loop and are using other features
    in Qt as well, this example can still be useful as a reference
    when creating your own window.
    """

    #: Name of the window
    name = "pyside2"
    #: PySide2 specific key constants
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
        self._app = QtWidgets.QApplication([])

        # Create the OpenGL widget
        self._widget = QtOpenGL.QGLWidget(gl)
        self.title = self._title

        # If fullscreen we change the window to match the desktop on the primary screen
        if self.fullscreen:
            rect = QtWidgets.QDesktopWidget().screenGeometry()
            self._width = rect.width()
            self._height = rect.height()
            self._buffer_width = rect.width() * self._widget.devicePixelRatio()
            self._buffer_height = rect.height() * self._widget.devicePixelRatio()

        if self.resizable:
            # Ensure a valid resize policy when window is resizable
            size_policy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding,
            )
            self._widget.setSizePolicy(size_policy)
            self._widget.resize(self.width, self.height)
        else:
            self._widget.setFixedSize(self.width, self.height)

        # Center the window on the screen if in window mode
        if not self.fullscreen:
            center_window_position = (
                self.position[0] - self.width / 2,
                self.position[1] - self.height / 2,
            )
            self._widget.move(*center_window_position)

        # Needs to be set before show()
        self._widget.resizeGL = self.resize

        self.cursor = self._cursor

        if self.fullscreen:
            self._widget.showFullScreen()
        else:
            self._widget.show()

        # We want mouse position events
        self._widget.setMouseTracking(True)

        # Override event functions in qt
        self._widget.keyPressEvent = self.key_pressed_event
        self._widget.keyReleaseEvent = self.key_release_event
        self._widget.mouseMoveEvent = self.mouse_move_event
        self._widget.mousePressEvent = self.mouse_press_event
        self._widget.mouseReleaseEvent = self.mouse_release_event
        self._widget.wheelEvent = self.mouse_wheel_event
        self._widget.closeEvent = self.close_event
        self._widget.showEvent = self.show_event
        self._widget.hideEvent = self.hide_event

        # Attach to the context
        self.init_mgl_context()

        # Ensure retina and 4k displays get the right viewport
        self._buffer_width = self._width * self._widget.devicePixelRatio()
        self._buffer_height = self._height * self._widget.devicePixelRatio()

        self.set_default_viewport()

    def _set_fullscreen(self, value: bool) -> None:
        if value:
            self._widget.showFullScreen()
        else:
            self._widget.showNormal()

    @property
    def size(self) -> Tuple[int, int]:
        """Tuple[int, int]: current window size.

        This property also support assignment::

            # Resize the window to 1000 x 1000
            window.size = 1000, 1000
        """
        return self._width, self._height

    @size.setter
    def size(self, value: Tuple[int, int]):
        pos = self.position
        self._widget.setGeometry(pos[0], pos[1], value[0], value[1])

    @property
    def position(self) -> Tuple[int, int]:
        """Tuple[int, int]: The current window position.

        This property can also be set to move the window::

            # Move window to 100, 100
            window.position = 100, 100
        """
        geo = self._widget.geometry()
        return geo.x(), geo.y()

    @position.setter
    def position(self, value: Tuple[int, int]):
        self._widget.setGeometry(value[0], value[1], self._width, self._height)

    @property
    def cursor(self) -> bool:
        """bool: Should the mouse cursor be visible inside the window?

        This property can also be assigned to::

            # Disable cursor
            window.cursor = False
        """
        return self._cursor

    @cursor.setter
    def cursor(self, value: bool):
        if value is True:
            self._widget.setCursor(QtCore.Qt.ArrowCursor)
        else:
            self._widget.setCursor(QtCore.Qt.BlankCursor)

        self._cursor = value

    @property
    def title(self) -> str:
        """str: Window title.

        This property can also be set::

            window.title = "New Title"
        """
        return self._title

    @title.setter
    def title(self, value: str):
        self._widget.setWindowTitle(value)
        self._title = value

    def swap_buffers(self) -> None:
        """Swap buffers, set viewport, trigger events and increment frame counter"""
        self._widget.swapBuffers()
        self.set_default_viewport()
        self._app.processEvents()
        self._frames += 1

    def resize(self, width: int, height: int) -> None:
        """Replacement for Qt's ``resizeGL`` method.

        Args:
            width: New window width
            height: New window height
        """
        self._width = width // self._widget.devicePixelRatio()
        self._height = height // self._widget.devicePixelRatio()
        self._buffer_width = width
        self._buffer_height = height

        if self._ctx:
            self.set_default_viewport()

        # Make sure we notify the example about the resize
        super().resize(self._buffer_width, self._buffer_height)

    def _handle_modifiers(self, mods):
        """Update modifiers"""
        self._modifiers.shift = bool(mods & QtCore.Qt.ShiftModifier)
        self._modifiers.ctrl = bool(mods & QtCore.Qt.ControlModifier)
        self._modifiers.alt = bool(mods & QtCore.Qt.AltModifier)

    def _set_icon(self, icon_path: str) -> None:
        self._widget.setWindowIcon(QtGui.QIcon(icon_path))

    def key_pressed_event(self, event):
        """Process Qt key press events forwarding them to standard methods

        Args:
            event: The qtevent instance
        """
        if self._exit_key is not None and event.key() == self._exit_key:
            self.close()

        if self._fs_key is not None and event.key() == self._fs_key:
            self.fullscreen = not self.fullscreen

        self._handle_modifiers(event.modifiers())
        self._key_pressed_map[event.key()] = True
        self.key_event_func(event.key(), self.keys.ACTION_PRESS, self._modifiers)

        text = event.text()
        if text.strip() or event.key() == self.keys.SPACE:
            self._unicode_char_entered_func(text)

    def key_release_event(self, event):
        """Process Qt key release events forwarding them to standard methods

        Args:
            event: The qtevent instance
        """
        self._handle_modifiers(event.modifiers())
        self._key_pressed_map[event.key()] = False
        self.key_event_func(event.key(), self.keys.ACTION_RELEASE, self._modifiers)

    def mouse_move_event(self, event) -> None:
        """Forward mouse cursor position events to standard methods

        Args:
            event: The qtevent instance
        """
        x, y = event.x(), event.y()
        dx, dy = self._calc_mouse_delta(x, y)

        if self.mouse_states.any:
            self._mouse_drag_event_func(x, y, dx, dy)
        else:
            self._mouse_position_event_func(x, y, dx, dy)

    def mouse_press_event(self, event) -> None:
        """Forward mouse press events to standard methods

        Args:
            event: The qtevent instance
        """
        self._handle_modifiers(event.modifiers())
        button = self._mouse_button_map.get(event.button())
        if button is None:
            return

        self._handle_mouse_button_state_change(button, True)
        self.mouse_press_event_func(event.x(), event.y(), button)

    def mouse_release_event(self, event) -> None:
        """Forward mouse release events to standard methods

        Args:
            event: The qtevent instance
        """
        self._handle_modifiers(event.modifiers())
        button = self._mouse_button_map.get(event.button())
        if button is None:
            return

        self._handle_mouse_button_state_change(button, False)
        self.mouse_release_event_func(event.x(), event.y(), button)

    def mouse_wheel_event(self, event):
        """Forward mouse wheel events to standard metods.

        From Qt docs:

        Returns the distance that the wheel is rotated, in eighths of a degree.
        A positive value indicates that the wheel was rotated forwards away from the user;
        a negative value indicates that the wheel was rotated backwards toward the user.

        Most mouse types work in steps of 15 degrees, in which case the delta value is a
        multiple of 120; i.e., 120 units * 1/8 = 15 degrees.

        However, some mice have finer-resolution wheels and send delta values that are less
        than 120 units (less than 15 degrees). To support this possibility, you can either
        cumulatively add the delta values from events until the value of 120 is reached,
        then scroll the widget, or you can partially scroll the widget in response to each
        wheel event.

        Args:
            event (QWheelEvent): Mouse wheel event
        """
        self._handle_modifiers(event.modifiers())
        point = event.angleDelta()
        self._mouse_scroll_event_func(point.x() / 120.0, point.y() / 120.0)

    def close_event(self, event) -> None:
        """The standard PyQt close events

        Args:
            event: The qtevent instance
        """
        self.close()

    def close(self):
        """Close the window"""
        super().close()
        self._close_func()

    def show_event(self, event):
        """The standard Qt show event"""
        self._iconify_func(False)

    def hide_event(self, event):
        """The standard Qt hide event"""
        self._iconify_func(True)

    def destroy(self) -> None:
        """Quit the Qt application to exit the window gracefully"""
        QtCore.QCoreApplication.instance().quit()
