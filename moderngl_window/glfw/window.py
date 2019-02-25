import glfw
import moderngl

from window.base import BaseWindow
from window.glfw.keys import Keys


class Window(BaseWindow):
    """
    Window based on GLFW
    """
    keys = Keys

    def __init__(self, **kwargs):
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
        glfw.window_hint(glfw.DOUBLEBUFFER, True)
        glfw.window_hint(glfw.DEPTH_BITS, 24)
        glfw.window_hint(glfw.SAMPLES, self.samples)

        monitor = None
        if self.fullscreen:
            # Use the primary monitors current resolution
            monitor = glfw.get_primary_monitor()
            mode = glfw.get_video_mode(monitor)
            self.width, self.height = mode.size.width, mode.size.height

            # Make sure video mode switching will not happen by
            # matching the desktops current video mode
            glfw.window_hint(glfw.RED_BITS, mode.bits.red)
            glfw.window_hint(glfw.GREEN_BITS, mode.bits.green)
            glfw.window_hint(glfw.BLUE_BITS, mode.bits.blue)
            glfw.window_hint(glfw.REFRESH_RATE, mode.refresh_rate)

        self.window = glfw.create_window(self.width, self.height, self.title, monitor, None)

        if not self.window:
            glfw.terminate()
            raise ValueError("Failed to create window")

        if not self.cursor:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        self.buffer_width, self.buffer_height = glfw.get_framebuffer_size(self.window)
        glfw.make_context_current(self.window)

        if self.vsync:
            glfw.swap_interval(1)

        glfw.set_key_callback(self.window, self.key_event_callback)
        glfw.set_cursor_pos_callback(self.window, self.mouse_event_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        glfw.set_window_size_callback(self.window, self.window_resize_callback)

        self.ctx = moderngl.create_context(require=self.gl_version_code)
        self.print_context_info()
        self.set_default_viewport()

    def close(self):
        """
        Suggest to glfw the window should be closed soon
        """
        glfw.set_window_should_close(self.window, True)

    @property
    def is_closing(self):
        """
        Checks if the window is scheduled for closing
        """
        return glfw.window_should_close(self.window)

    def swap_buffers(self):
        """
        Swap buffers, increment frame counter and pull events
        """
        glfw.swap_buffers(self.window)
        self.frames += 1
        glfw.poll_events()

    def key_event_callback(self, window, key, scancode, action, mods):
        """
        Key event callback for glfw.
        Translates and forwards keyboard event to :py:func:`keyboard_event`

        Args:
            window: Window event origin
            key: The key that was pressed or released.
            scancode: The system-specific scancode of the key.
            action: GLFW_PRESS, GLFW_RELEASE or GLFW_REPEAT
            mods: Bit field describing which modifier keys were held down.
        """
        if key == self.keys.ESCAPE:
            self.close()

        self.example.key_event(key, action)

    def mouse_event_callback(self, window, xpos, ypos):
        """
        Mouse event callback from glfw.
        Translates the events forwarding them to :py:func:`cursor_event`.

        Args:
            window: The window
            xpos: viewport x pos
            ypos: viewport y pos
        """
        # screen coordinates relative to the top-left corner
        self.example.mouse_position_event(xpos, ypos)

    def mouse_button_callback(self, window, button, action, mods):
        """
        Handle mouse button events and forward them to the example
        """
        # Offset button index by 1 to make it match the other libraries
        button += 1
        # Support left and right mouse button for now
        if button not in [1, 2]:
            return

        xpos, ypos = glfw.get_cursor_pos(self.window)

        if action == glfw.PRESS:
            self.example.mouse_press_event(xpos, ypos, button)
        else:
            self.example.mouse_release_event(xpos, ypos, button)

    def window_resize_callback(self, window, width, height):
        """
        Window resize callback for glfw

        Args:
            window: The window
            width: New width
            height: New height
        """
        self.width, self.height = width, height
        self.buffer_width, self.buffer_height = glfw.get_framebuffer_size(self.window)
        self.set_default_viewport()

        super().resize(self.buffer_width, self.buffer_height)

    def destroy(self):
        """
        Gracefully terminate GLFW.
        This will also properly terminate the window and context
        """
        glfw.terminate()
