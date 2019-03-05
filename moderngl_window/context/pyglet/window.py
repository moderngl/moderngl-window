import platform

import moderngl
import pyglet

from moderngl_window.context.pyglet.keys import Keys
from moderngl_window.context.base import BaseWindow


if platform.system() == "Darwin":
    raise RuntimeError((
        "Pyglet 1.x do not support OpenGL core contexts "
        "and will only be able to support version 2.1 on OS X.\n"
        "Please use another window driver for this platform "
        "until a pyglet 2.x window is created"
))


class Window(BaseWindow):
    """
    Window based on Pyglet 1.x.

    This pyglet version is not able to create forward compatible
    core contexts and do not work on OS X until 2.x is out.
    """
    keys = Keys

    # Pyglet supports three mouse buttons
    # Pyglet key id -> Generic key id
    _mouse_button_map = {
        1: 1,
        4: 2,
        2: 3,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        pyglet.options['debug_gl'] = False
        pyglet.options['shadow_window'] = False

        # Set context parameters
        config = pyglet.gl.Config()
        config.double_buffer = True
        config.major_version = self.gl_version[0]
        config.minor_version = self.gl_version[1]
        config.forward_compatible = True
        # MISSING: Core context flag
        config.sample_buffers = 1 if self.samples > 1 else 0
        config.samples = self.samples

        # Obtain the default destop screen's resolution
        if self.fullscreen:
            platform = pyglet.window.get_platform()
            display = platform.get_default_display()
            screen = display.get_default_screen()
            self._width, self._height = screen.width, screen.height

        self._window = PygletWrapper(
            width=self.width, height=self.height,
            caption=self.title,
            resizable=self.resizable,
            vsync=self.vsync,
            fullscreen=self.fullscreen,
        )

        self._window.set_mouse_visible(self.cursor)

        # Override the default event callbacks in pyglet
        # These functions are identified by name
        self._window.event(self.on_key_press)
        self._window.event(self.on_key_release)
        self._window.event(self.on_mouse_motion)
        self._window.event(self.on_resize)
        self._window.event(self.on_mouse_press)
        self._window.event(self.on_mouse_release)

        self._ctx = moderngl.create_context(require=self.gl_version_code)
        self.set_default_viewport()
        self.print_context_info()

    @property
    def is_closing(self):
        """
        Check pyglet's internal exit state
        """
        return self._window.has_exit

    def close(self):
        """
        Close the pyglet window directly
        """
        self._window.close()

    def swap_buffers(self):
        """
        Swap buffers, increment frame counter and pull events
        """
        self._window.flip()
        self._frames += 1
        self._window.dispatch_events()

    def on_key_press(self, symbol, modifiers):
        """
        Pyglet specific key press callback.
        Forwards and translates the events to the example
        """
        self._key_pressed_map[symbol] = True
        self._key_event_func(symbol, self.keys.ACTION_PRESS)

    def on_key_release(self, symbol, modifiers):
        """
        Pyglet specific key release callback.
        Forwards and translates the events to the example
        """
        self._key_pressed_map[symbol] = False
        self._key_event_func(symbol, self.keys.ACTION_RELEASE)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Pyglet specific mouse motion callback.
        Forwards and traslates the event to the example
        """
        # Screen coordinates relative to the lower-left corner
        # so we have to flip the y axis to make this consistent with
        # other window libraries
        self._mouse_position_event_func(x, self._buffer_height - y)

    def on_mouse_press(self, x: int, y: int, button, mods):
        """
        Handle mouse press events and forward to example window
        """
        button = self._mouse_button_map.get(button, None)
        if button is not None:
            self._mouse_press_event_func(
                x, self._buffer_height - y,
                button,
            )

    def on_mouse_release(self, x: int, y: int, button, mods):
        """
        Handle mouse release events and forward to example window
        """
        button = self._mouse_button_map.get(button, None)
        if button is not None:
            self._mouse_release_event_func(
                x, self._buffer_height - y,
                button,
            )

    def on_resize(self, width: int, height: int):
        """
        Pyglet specific callback for window resize events.
        """
        self._width, self._height = width, height
        self._buffer_width, self._buffer_height = width, height
        self.set_default_viewport()

        super().resize(self._buffer_width, self._buffer_height)

    def destroy(self):
        """Destroy the pyglet window"""
        # Nothing to do here as close() covers this for pyglet already
        pass


class PygletWrapper(pyglet.window.Window):
    """
    Block out some window methods so pyglet don't trigger GL errors
    """

    def on_resize(self, width, height):
        """
        Block out the resize method.
        For some reason pyglet calls this triggering errors.
        """
        pass

    def on_draw(self):
        """
        Block out the dfault draw method to avoid GL errors.
        """
        pass
