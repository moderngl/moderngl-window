import platform

import pyglet

# On OS X we need to disable the shadow context
# because the 2.1 shadow context cannot be upgrade to a 3.3+ core
if platform.system() == "Darwin":
    pyglet.options["shadow_window"] = False

pyglet.options["debug_gl"] = False
from pathlib import Path  # noqa
from typing import Any, Union  # noqa

from moderngl_window.context.base import BaseWindow  # noqa: E402
from moderngl_window.context.pyglet.keys import Keys  # noqa: E402


class Window(BaseWindow):
    """
    Window based on Pyglet 1.4.x
    """

    #: Name of the window
    name = "pyglet"
    #: Pyglet specific key constants
    keys = Keys

    # pyglet button id -> universal button id
    _mouse_button_map = {
        1: 1,
        4: 2,
        2: 3,
    }

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

        config = pyglet.gl.Config(
            major_version=self.gl_version[0],
            minor_version=self.gl_version[1],
            forward_compatible=True,
            red_size=8,
            green_size=8,
            blue_size=8,
            alpha_size=8,
            stencil_size=8,
            depth_size=24,
            double_buffer=True,
            sample_buffers=1 if self.samples > 1 else 0,
            samples=self.samples,
        )

        if self.fullscreen:
            if hasattr(pyglet, 'canvas'):
                display = pyglet.canvas.get_display()
            else:
                display = pyglet.display.get_display()
            screen = display.get_default_screen()
            self._width, self._height = screen.width, screen.height

        self._window = PygletWrapper(
            width=self._width,
            height=self._height,
            caption=self._title,
            resizable=self._resizable,
            visible=self._visible,
            vsync=self._vsync,
            fullscreen=self._fullscreen,
            config=config,
            file_drops=True and platform.system() != "Darwin",
        )

        self.cursor = self._cursor

        self._window.event(self.on_key_press)
        self._window.event(self.on_key_release)
        self._window.event(self.on_mouse_motion)
        self._window.event(self.on_mouse_drag)
        self._window.event(self.on_resize)
        self._window.event(self.on_close)
        self._window.event(self.on_mouse_press)
        self._window.event(self.on_mouse_release)
        self._window.event(self.on_mouse_scroll)
        self._window.event(self.on_text)
        self._window.event(self.on_show)
        self._window.event(self.on_hide)
        self._window.event(self.on_file_drop)

        self.init_mgl_context()
        self._buffer_width, self._buffer_height = self._window.get_framebuffer_size()
        self.set_default_viewport()

    def _set_fullscreen(self, value: bool) -> None:
        self._window.set_fullscreen(value)

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
        self._window.set_size(value[0], value[1])

    @property
    def position(self) -> tuple[int, int]:
        """tuple[int, int]: The current window position.

        This property can also be set to move the window::

            # Move window to 100, 100
            window.position = 100, 100
        """
        return self._window.get_location()

    @position.setter
    def position(self, value: tuple[int, int]) -> None:
        self._window.set_location(value[0], value[1])

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
        self._window.set_visible(value)

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
        self._window.set_mouse_visible(value)
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
        self._window.set_exclusive_mouse(value)
        self._mouse_exclusivity = value

    @property
    def title(self) -> str:
        """str: Window title.

        This property can also be set::

            window.title = "New Title"
        """
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._window.set_caption(value)
        self._title = value

    @property
    def is_closing(self) -> bool:
        """Check pyglet's internal exit state"""
        return self._window.has_exit or super().is_closing

    @is_closing.setter
    def is_closing(self, value: bool) -> None:
        self._close = value

    def close(self) -> None:
        """Close the pyglet window directly"""
        self.is_closing = True
        self._window.close()
        super().close()

    def swap_buffers(self) -> None:
        """Swap buffers, increment frame counter and pull events"""
        self._window.flip()
        self._frames += 1
        self._window.dispatch_events()

    def _handle_modifiers(self, mods: int) -> None:
        """Update key modifier states"""
        self._modifiers.shift = mods & 1 == 1
        self._modifiers.ctrl = mods & 2 == 2
        self._modifiers.alt = mods & 4 == 4

    def _set_icon(self, icon_path: Path) -> None:
        icon = pyglet.image.load(icon_path)
        self._window.set_icon(icon)

    def _set_vsync(self, value: bool) -> None:
        self._window.set_vsync(value)

    def on_key_press(self, symbol: int, modifiers: int) -> bool:
        """Pyglet specific key press callback.

        Forwards and translates the events to the standard methods.

        Args:
            symbol: The symbol of the pressed key
            modifiers: Modifier state (shift, ctrl etc.)
        """
        if self._exit_key is not None and symbol == self._exit_key:
            self.close()

        if self._fs_key is not None and symbol == self._fs_key:
            self.fullscreen = not self.fullscreen

        self._key_pressed_map[symbol] = True
        self._handle_modifiers(modifiers)
        self._key_event_func(symbol, self.keys.ACTION_PRESS, self._modifiers)

        return pyglet.event.EVENT_HANDLED

    def on_text(self, text: str) -> None:
        """Pyglet specific text input callback

        Forwards and translates the events to the standard methods.

        Args:
            text (str): The unicode character entered
        """
        self._unicode_char_entered_func(text)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Pyglet specific key release callback.

        Forwards and translates the events to standard methods.

        Args:
            symbol: The symbol of the pressed key
            modifiers: Modifier state (shift, ctrl etc.)
        """
        self._key_pressed_map[symbol] = False
        self._handle_modifiers(modifiers)
        self._key_event_func(symbol, self.keys.ACTION_RELEASE, self._modifiers)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        """Pyglet specific mouse motion callback.

        Forwards and translates the event to the standard methods.

        Args:
            x: x position of the mouse
            y: y position of the mouse
            dx: delta x position
            dy: delta y position of the mouse
        """
        # NOTE: Screen coordinates relative to the lower-left corner
        # so we have to flip the y axis to make this consistent with
        # other window libraries
        self._mouse_position_event_func(x, self._height - y, dx, -dy)

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int) -> None:
        """Pyglet specific mouse drag event.

        When a mouse button is pressed this is the only way
        to capture mouse position events
        """
        self._handle_modifiers(modifiers)
        self._mouse_drag_event_func(x, self._height - y, dx, -dy)

    def on_mouse_press(self, x: int, y: int, button: int, mods: int) -> None:
        """Handle mouse press events and forward to standard methods

        Args:
            x: x position of the mouse when pressed
            y: y position of the mouse when pressed
            button: The pressed button
            mods: Modifiers
        """
        self._handle_modifiers(mods)
        button = self._mouse_button_map.get(button, -1)
        if button != -1:
            self._handle_mouse_button_state_change(button, True)
            self._mouse_press_event_func(
                x,
                self._height - y,
                button,
            )

    def on_mouse_release(self, x: int, y: int, button: int, mods: int) -> None:
        """Handle mouse release events and forward to standard methods

        Args:
            x: x position when mouse button was released
            y: y position when mouse button was released
            button: The button pressed
            mods: Modifiers
        """
        button = self._mouse_button_map.get(button, -1)
        if button != -1:
            self._handle_mouse_button_state_change(button, False)
            self._mouse_release_event_func(
                x,
                self._height - y,
                button,
            )

    def on_mouse_scroll(self, x: int, y: int, x_offset: float, y_offset: float) -> None:
        """Handle mouse wheel.

        Args:
            x_offset (float): X scroll offset
            y_offset (float): Y scroll offset
        """
        self._handle_modifiers(0)  # No modifiers available
        self.mouse_scroll_event_func(x_offset, y_offset)

    def on_resize(self, width: int, height: int) -> None:
        """Pyglet specific callback for window resize events forwarding to standard methods

        Args:
            width: New window width
            height: New window height
        """
        self._width, self._height = width, height
        self._buffer_width, self._buffer_height = self._window.get_framebuffer_size()
        self.set_default_viewport()

        super().resize(self._buffer_width, self._buffer_height)

    def on_close(self) -> None:
        """Pyglet specific window close callback"""
        self._close_func()

    def on_show(self) -> None:
        """Called when window first appear or restored from hidden state"""
        self._visible = True
        self._iconify_func(False)

    def on_hide(self) -> None:
        """Called when window is minimized"""
        self._visible = False
        self._iconify_func(True)

    def on_file_drop(self, x: int, y: int, paths: list[Union[str, Path]]) -> None:
        """Called when files dropped onto the window

        Args:
            x (int): X location in window where file was dropped
            y (int): Y location in window where file was dropped
            paths (list): List of file paths dropped
        """
        # pyglet coordinate origin is in the bottom left corner of the window
        # mglw coordinate origin is in the top left corner of the window
        # convert pyglet coordinates to mglw coordinates:
        (x, y) = self.convert_window_coordinates(x, y, y_flipped=True)
        self._files_dropped_event_func(x, y, paths)

    def destroy(self) -> None:
        """Destroy the pyglet window"""
        pass


class PygletWrapper(pyglet.window.Window):
    """Block out some window methods so pyglet don't trigger GL errors"""

    def on_resize(self, width: int, height: int) -> None:
        """Block out the resize method.
        For some reason pyglet calls this triggering errors.
        """
        pass

    def on_draw(self) -> None:
        """Block out the default draw method to avoid GL errors"""
        pass
