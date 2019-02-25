import platform

import moderngl
import pyglet

from window.pyglet.keys import Keys
from window.base import BaseWindow


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Disable all error checking
        pyglet.options['debug_gl'] = False

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
            self.width, self.height = screen.width, screen.height

        # Create window wrapper
        self.window = PygletWrapper(
            width=self.width, height=self.height,
            caption=self.title,
            resizable=self.resizable,
            vsync=self.vsync,
            fullscreen=self.fullscreen,
        )

        # Show/hide mouse cursor
        self.window.set_mouse_visible(self.cursor)

        # Override the default event callbacks
        self.window.event(self.on_key_press)
        self.window.event(self.on_key_release)
        self.window.event(self.on_mouse_motion)
        self.window.event(self.on_resize)
        self.window.event(self.on_mouse_press)
        self.window.event(self.on_mouse_release)

        self.ctx = moderngl.create_context(require=self.gl_version_code)
        self.set_default_viewport()
        self.print_context_info()

    @property
    def is_closing(self):
        """
        Check pyglet's internal exit state
        """
        return self.window.has_exit

    def close(self):
        """
        Close the pyglet window directly
        """
        self.window.close()

    def swap_buffers(self):
        """
        Swap buffers, increment frame counter and pull events
        """
        self.window.flip()
        self.frames += 1
        self.window.dispatch_events()

    def on_key_press(self, symbol, modifiers):
        """
        Pyglet specific key press callback.
        Forwards and translates the events to the example
        """
        self.example.key_event(symbol, self.keys.ACTION_PRESS)

    def on_key_release(self, symbol, modifiers):
        """
        Pyglet specific key release callback.
        Forwards and translates the events to the example
        """
        self.example.key_event(symbol, self.keys.ACTION_RELEASE)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Pyglet specific mouse motion callback.
        Forwards and traslates the event to the example
        """
        # Screen coordinates relative to the lower-left corner
        # so we have to flip the y axis to make this consistent with
        # other window libraries
        self.example.mouse_position_event(x, self.buffer_height - y)

    def on_mouse_press(self, x: int, y: int, button, mods):
        """
        Handle mouse press events and forward to example window
        """
        if button in [1, 4]:
            self.example.mouse_press_event(
                x, self.buffer_height - y,
                1 if button == 1 else 2,
            )

    def on_mouse_release(self, x: int, y: int, button, mods):
        """
        Handle mouse release events and forward to example window
        """
        if button in [1, 4]:
            self.example.mouse_release_event(
                x, self.buffer_height - y,
                1 if button == 1 else 2,
            )

    def on_resize(self, width: int, height: int):
        """
        Pyglet specific callback for window resize events.
        """
        self.width, self.height = width, height
        self.buffer_width, self.buffer_height = width, height
        self.set_default_viewport()

        super().resize(self.buffer_width, self.buffer_height)

    def destroy(self):
        """
        Nothing to do here as close() is doing the cleanup
        """
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
