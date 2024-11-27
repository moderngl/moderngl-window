import glfw

from PIL import Image
from typing import Any
from pathlib import Path

from moderngl_window.context.base import BaseWindow
from moderngl_window.context.glfw.keys import Keys, GLFW_key

class Window(BaseWindow):
    """
    Window based on GLFW
    """

    #: Name of the window
    name = "glfw"
    #: GLFW specific key constants
    keys = Keys

    # GLFW do support other buttons, but we are limited by other libraries
    _mouse_button_map = {
        0: 1,
        1: 2,
        2: 3,
    }

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

        if not glfw.init():
            raise ValueError("Failed to initialize glfw")

        # Configure the OpenGL context
        glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.NATIVE_CONTEXT_API)
        glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, self.gl_version[0])
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, self.gl_version[1])
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.RESIZABLE, self.resizable)
        glfw.window_hint(glfw.VISIBLE, self.visible)
        glfw.window_hint(glfw.DOUBLEBUFFER, True)
        glfw.window_hint(glfw.DEPTH_BITS, 24)
        glfw.window_hint(glfw.STENCIL_BITS, 8)
        glfw.window_hint(glfw.SAMPLES, self.samples)
        glfw.window_hint(glfw.SCALE_TO_MONITOR, glfw.TRUE)

        monitor = None

        self._window = glfw.create_window(self.width, self.height, self.title, monitor, None)
        self._has_focus = True

        if self.fullscreen:
            self._set_fullscreen(True)

        if not self._window:
            glfw.terminate()
            raise ValueError("Failed to create window")

        self.cursor = self._cursor

        self._buffer_width, self._buffer_height = glfw.get_framebuffer_size(self._window)
        glfw.make_context_current(self._window)

        if self.vsync:
            glfw.swap_interval(1)
        else:
            glfw.swap_interval(0)

        glfw.set_key_callback(self._window, self.glfw_key_event_callback)
        glfw.set_cursor_pos_callback(self._window, self.glfw_mouse_event_callback)
        glfw.set_mouse_button_callback(self._window, self.glfw_mouse_button_callback)
        glfw.set_scroll_callback(self._window, self.glfw_mouse_scroll_callback)
        glfw.set_window_size_callback(self._window, self.glfw_window_resize_callback)
        glfw.set_char_callback(self._window, self.glfw_char_callback)
        glfw.set_window_focus_callback(self._window, self.glfw_window_focus)
        glfw.set_cursor_enter_callback(self._window, self.glfw_cursor_enter)
        glfw.set_window_iconify_callback(self._window, self.glfw_window_iconify)
        glfw.set_window_close_callback(self._window, self.glfw_window_close)

        self.init_mgl_context()
        self.set_default_viewport()

    def _set_fullscreen(self, value: bool) -> None:
        monitor = glfw.get_primary_monitor()
        mode = glfw.get_video_mode(monitor)
        refresh_rate = mode.refresh_rate if self.vsync else glfw.DONT_CARE
        self.resizable = not value
        glfw.window_hint(glfw.RESIZABLE, self.resizable)

        if value:
            # enable fullscreen
            self._non_fullscreen_size = self.width, self.height
            self._non_fullscreen_position = self.position
            glfw.set_window_monitor(
                self._window,
                monitor,
                0,
                0,
                mode.size.width,
                mode.size.height,
                refresh_rate,
            )

            glfw.window_hint(glfw.RED_BITS, mode.bits.red)
            glfw.window_hint(glfw.GREEN_BITS, mode.bits.green)
            glfw.window_hint(glfw.BLUE_BITS, mode.bits.blue)
            glfw.window_hint(glfw.REFRESH_RATE, mode.refresh_rate)

        else:
            # disable fullscreen
            glfw.set_window_monitor(
                self._window,
                None,
                *self._non_fullscreen_position,
                *self._non_fullscreen_size,
                refresh_rate,
            )

        if self.vsync:
            glfw.swap_interval(1)
        else:
            glfw.swap_interval(0)

    def _set_vsync(self, value: bool) -> None:
        glfw.swap_interval(value)

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
        glfw.set_window_size(self._window, value[0], value[1])

    @property
    def position(self) -> tuple[int, int]:
        """tuple[int, int]: The current window position.

        This property can also be set to move the window::

            # Move window to 100, 100
            window.position = 100, 100
        """
        return glfw.get_window_pos(self._window)

    @position.setter
    def position(self, value: tuple[int, int]) -> None:
        self._position = glfw.set_window_pos(self._window, value[0], value[1])

    @property
    def visible(self) -> bool:
        """bool: Is the window visible?

        This property can also be set::

            # Hide or show the window
            window.visible = False
        """
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        self._visible = value
        if value:
            glfw.show_window(self._window)
        else:
            glfw.hide_window(self._window)

    @property
    def cursor(self) -> bool:
        """bool: Should the mouse cursor be visible inside the window?

        This property can also be assigned to::

            # Disable cursor
            window.cursor = False
        """
        return self._cursor

    @cursor.setter
    def cursor(self, value: bool) -> None:
        if not self.mouse_exclusivity:
            if value is True:
                glfw.set_input_mode(self._window, glfw.CURSOR, glfw.CURSOR_NORMAL)
            elif value is False:
                glfw.set_input_mode(self._window, glfw.CURSOR, glfw.CURSOR_HIDDEN)

        self._cursor = value

    @property
    def mouse_exclusivity(self) -> bool:
        """bool: If mouse exclusivity is enabled.

        When you enable mouse-exclusive mode, the mouse cursor is no longer
        available. It is not merely hidden – no amount of mouse movement
        will make it leave your application. This is for example useful
        when you don't want the mouse leaving the screen when rotating
        a 3d scene.

        This property can also be set::

            window.mouse_exclusivity = True
        """
        return self._mouse_exclusivity

    @mouse_exclusivity.setter
    def mouse_exclusivity(self, value: bool) -> None:
        self._mouse_exclusivity = value
        if value is True:
            self._mouse_pos = glfw.get_cursor_pos(self._window)
            glfw.set_input_mode(self._window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        else:
            self.cursor = self._cursor

    @property
    def title(self) -> str:
        """str: Window title.

        This property can also be set::

            window.title = "New Title"
        """
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        glfw.set_window_title(self._window, value)
        self._title = value

    def close(self) -> None:
        """Suggest to glfw the window should be closed soon"""
        self.is_closing = True
        self._close_func()

    @property
    def is_closing(self) -> bool:
        """bool: Checks if the window is scheduled for closing"""
        return glfw.window_should_close(self._window)

    @is_closing.setter
    def is_closing(self, value: bool) -> None:
        glfw.set_window_should_close(self._window, value)

    def swap_buffers(self) -> None:
        """Swap buffers, increment frame counter and pull events"""
        glfw.swap_buffers(self._window)
        self._frames += 1
        glfw.poll_events()

    def _handle_modifiers(self, mods: GLFW_key) -> None:
        """Checks key modifiers"""
        self._modifiers.shift = mods & 1 == 1
        self._modifiers.ctrl = mods & 2 == 2
        self._modifiers.alt = mods & 4 == 4

    def _set_icon(self, icon_path: Path) -> None:
        image = Image.open(icon_path)
        glfw.set_window_icon(self._window, 1, image)

    def glfw_key_event_callback(self, window: Any, key: GLFW_key, scancode: int, action: GLFW_key, mods: GLFW_key) -> None:
        """Key event callback for glfw.
        Translates and forwards keyboard event to :py:func:`keyboard_event`

        Args:
            window: Window event origin
            key: The key that was pressed or released.
            scancode: The system-specific scancode of the key.
            action: ``GLFW_PRESS``, ``GLFW_RELEASE`` or ``GLFW_REPEAT``
            mods: Bit field describing which modifier keys were held down.
        """
        if self.exit_key is not None and key == self._exit_key:
            self.close()

        if action == self.keys.ACTION_PRESS and self._fs_key is not None and key == self._fs_key:
            self.fullscreen = not self.fullscreen

        self._handle_modifiers(mods)

        if action == self.keys.ACTION_PRESS:
            self._key_pressed_map[key] = True
        elif action == self.keys.ACTION_RELEASE:
            self._key_pressed_map[key] = False

        self._key_event_func(key, action, self._modifiers)

    def glfw_mouse_event_callback(self, window: Any, xpos: float, ypos: float) -> None:
        """Mouse position event callback from glfw.
        Translates the events forwarding them to :py:func:`cursor_event`.

        Screen coordinates relative to the top-left corner

        Args:
            window: The window
            xpos: viewport x pos
            ypos: viewport y pos
        """
        xpos, ypos = int(xpos), int(ypos)
        dx, dy = self._calc_mouse_delta(xpos, ypos)

        if self.mouse_states.any:
            self._mouse_drag_event_func(xpos, ypos, dx, dy)
        else:
            self._mouse_position_event_func(xpos, ypos, dx, dy)

    def glfw_mouse_button_callback(self, window: Any, button: GLFW_key, action: GLFW_key, mods: GLFW_key) -> None:
        """Handle mouse button events and forward them to the example

        Args:
            window: The window
            button: The button creating the event
            action: Button action (press or release)
            mods: They modifiers such as ctrl or shift
        """
        self._handle_modifiers(mods)
        button = self._mouse_button_map.get(button, -1)
        if button == -1:
            return

        xpos, ypos = glfw.get_cursor_pos(self._window)

        if action == glfw.PRESS:
            self._handle_mouse_button_state_change(button, True)
            self._mouse_press_event_func(xpos, ypos, button)
        else:
            self._handle_mouse_button_state_change(button, False)
            self._mouse_release_event_func(xpos, ypos, button)

    def glfw_mouse_scroll_callback(self, window: Any, x_offset: float, y_offset: float) -> None:
        """Handle mouse scroll events and forward them to the example

        Args:
            window: The window
            x_offset (float): x wheel offset
            y_offest (float): y wheel offset
        """
        self._mouse_scroll_event_func(x_offset, y_offset)

    def glfw_char_callback(self, window: Any, codepoint: int) -> None:
        """Handle text input (only unicode charaters)

        Args:
            window: The glfw window
            codepoint (int): The unicode codepoint
        """
        self._unicode_char_entered_func(chr(codepoint))

    def glfw_window_resize_callback(self, window: Any, width: int, height: int) -> None:
        """
        Window resize callback for glfw

        Args:
            window: The window
            width: New width
            height: New height
        """
        self._width, self._height = width, height
        self._buffer_width, self._buffer_height = glfw.get_framebuffer_size(self._window)
        self.set_default_viewport()

        super().resize(self._buffer_width, self._buffer_height)

    def glfw_window_focus(self, window: Any, focused: int) -> None:
        """Called when the window focus is changed.

        Args:
            window: The window instance
            focused (int): 0: de-focus, 1: focused
        """
        self._has_focus = True if focused == 1 else False

    def glfw_cursor_enter(self, window: Any, enter: int) -> None:
        """called when the cursor enters or leaves the content area of the window.

        Args:
            window: the window instance
            enter (int): 0: leave, 1: enter
        """
        pass

    def glfw_window_iconify(self, window: Any, iconified: int) -> None:
        """Called when the window is minimized or restored.

        Args:
            window: The window
            iconified (int): 1 = minimized, 0 = restored.
        """
        self._iconify_func(True if iconified == 1 else False)

    def glfw_window_close(self, window: Any) -> None:
        """Called when the window is closed"""
        self.close()

    def destroy(self) -> None:
        """Gracefully terminate GLFW"""
        glfw.terminate()
