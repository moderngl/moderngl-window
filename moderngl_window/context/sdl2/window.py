import sdl2
import sdl2.ext
import sdl2.video
import moderngl

from moderngl_window.context.base import BaseWindow
from moderngl_window.context.sdl2.keys import Keys


class Window(BaseWindow):
    """
    Basic window implementation using SDL2.
    """
    keys = Keys

    # SDL2 supports more buttons but we are limited by other libraries
    _mouse_button_map = {
        1: 1,
        3: 2,
        2: 3,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            raise ValueError("Failed to initialize sdl2")

        # Configure OpenGL context
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, self.gl_version[0])
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, self.gl_version[1])
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, 1)
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)

        # Display/hide mouse cursor
        sdl2.SDL_ShowCursor(sdl2.SDL_ENABLE if self.cursor else sdl2.SDL_DISABLE)

        # Configure multisampling
        if self.samples > 1:
            sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLEBUFFERS, 1)
            sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLESAMPLES, self.samples)

        # Built the window flags
        flags = sdl2.SDL_WINDOW_OPENGL
        if self.fullscreen:
            # Use primary desktop screen resolution
            flags |= sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP
        else:
            if self.resizable:
                flags |= sdl2.SDL_WINDOW_RESIZABLE

        # Create the window
        self._window = sdl2.SDL_CreateWindow(
            self.title.encode(),
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            self.width,
            self.height,
            flags,
        )

        if not self._window:
            raise ValueError("Failed to create window:", sdl2.SDL_GetError())

        self._context = sdl2.SDL_GL_CreateContext(self._window)
        sdl2.video.SDL_GL_SetSwapInterval(1 if self.vsync else 0)

        self._ctx = moderngl.create_context(require=self.gl_version_code)
        self.set_default_viewport()

    def swap_buffers(self):
        """
        Swap buffers, set viewport, trigger events and increment frame counter
        """
        sdl2.SDL_GL_SwapWindow(self._window)
        self.set_default_viewport()
        self.process_events()
        self._frames += 1

    def resize(self, width, height):
        """Update internal size values"""
        self._width = width
        self._height = height
        self._buffer_width, self._buffer_height = self._width, self._height
        self.set_default_viewport()

        super().resize(self._buffer_width, self._buffer_height)

    def process_events(self):
        """Handle all queued events in sdl2"""
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_MOUSEMOTION:
                self._mouse_position_event_func(event.motion.x, event.motion.y)

            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                button = self._mouse_button_map.get(event.button.button, None)
                if button is not None:
                    self._mouse_release_event_func(
                        event.motion.x, event.motion.y,
                        button,
                    )

            elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                button = self._mouse_button_map.get(event.button.button, None)
                if button is not None:
                    self._mouse_press_event_func(
                        event.motion.x, event.motion.y,
                        button,
                    )

            elif event.type in [sdl2.SDL_KEYDOWN, sdl2.SDL_KEYUP]:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    self.close()

                if event.type == sdl2.SDL_KEYDOWN:
                    self._key_pressed_map[event.key.keysym.sym] = True
                elif event.type == sdl2.SDL_KEYUP:
                    self._key_pressed_map[event.key.keysym.sym] = False

                self._key_event_func(event.key.keysym.sym, event.type)

            elif event.type == sdl2.SDL_QUIT:
                self.close()

            elif event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    self.resize(event.window.data1, event.window.data2)

    def destroy(self):
        """Gracefully close the window"""
        sdl2.SDL_GL_DeleteContext(self._context)
        sdl2.SDL_DestroyWindow(self._window)
        sdl2.SDL_Quit()
