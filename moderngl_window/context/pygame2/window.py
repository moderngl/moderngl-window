from typing import Tuple
from ctypes import c_int, c_char_p
import pygame
import pygame.display
import pygame.event

from moderngl_window.context.base import BaseWindow
from moderngl_window.context.pygame2.keys import Keys


class Window(BaseWindow):
    """
    Basic window implementation using SDL2.
    """
    #: pygame specific key constants
    keys = Keys

    _mouse_button_map = {
        1: 1,
        3: 2,
        2: 3,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # TODO: We initialize all modules for now. Probably not needed.
        if pygame.init()[1] != 0:
            raise ValueError("Failed to initialize pygame")

        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, self.gl_version[0])
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, self.gl_version[1])
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, 1)
        pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)

        self.cursor = self._cursor

        if self.samples > 1:
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, self.samples)

        flags = pygame.OPENGL
        if self.fullscreen:
            flags |= pygame.FULLSCREEN
        else:
            if self.resizable:
                flags |= pygame.RESIZABLE

        pygame.display.set_mode(
            (self._width, self._height),
            flags=flags,
            depth=24,
        )
        pygame.display
        # self._window = sdl2.SDL_CreateWindow(
        #     self.title.encode(),
        #     sdl2.SDL_WINDOWPOS_UNDEFINED,
        #     sdl2.SDL_WINDOWPOS_UNDEFINED,
        #     self.width,
        #     self.height,
        #     flags,
        # )

        # if not self._window:
        #     raise ValueError("Failed to create window:", sdl2.SDL_GetError())

        # self._context = sdl2.SDL_GL_CreateContext(self._window)

        # sdl2.video.SDL_GL_SetSwapInterval(1 if self.vsync else 0)

        self.init_mgl_context()

        self.set_default_viewport()

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
        sdl2.SDL_SetWindowSize(self._window, value[0], value[1])
        # SDL_SetWindowSize don't trigger a resize event
        self.resize(value[0], value[1])

    @property
    def position(self) -> Tuple[int, int]:
        """Tuple[int, int]: The current window position.

        This property can also be set to move the window::

            # Move window to 100, 100
            window.position = 100, 100
        """
        x = c_int(0)
        y = c_int(0)
        sdl2.SDL_GetWindowPosition(self._window, x, y)
        return x.value, y.value

    @position.setter
    def position(self, value: Tuple[int, int]):
        sdl2.SDL_SetWindowPosition(self._window, value[0], value[1])

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
        pygame.mouse.set_visible(value)
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
    def mouse_exclusivity(self, value: bool):
        # if value is True:
        #     sdl2.SDL_SetRelativeMouseMode(sdl2.SDL_TRUE)
        # else:
        #     sdl2.SDL_SetRelativeMouseMode(sdl2.SDL_FALSE)

        self._mouse_exclusivity = value

    @property
    def title(self) -> str:
        """str: Window title.

        This property can also be set::

            window.title = "New Title"
        """
        return self._title

    @title.setter
    def title(self, value: str):
        pygame.display.set_caption(value)
        self._title = value

    def swap_buffers(self) -> None:
        """Swap buffers, set viewport, trigger events and increment frame counter"""
        pygame.display.flip()
        self.set_default_viewport()
        self.process_events()
        self._frames += 1

    def resize(self, width, height) -> None:
        """Resize callback

        Args:
            width: New window width
            height: New window height
        """
        self._width = width
        self._height = height
        self._buffer_width, self._buffer_height = self._width, self._height
        self.set_default_viewport()

        super().resize(self._buffer_width, self._buffer_height)

    def _handle_mods(self) -> None:
        """Update key mods"""
        mods = pygame.key.get_mods()
        self._modifiers.shift = mods & pygame.KMOD_SHIFT
        self._modifiers.ctrl = mods & pygame.KMOD_CTRL

    def process_events(self) -> None:
        """Handle all queued events in sdl2 dispatching events to standard methods"""

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if self.mouse_states.any:
                    self._mouse_drag_event_func(
                        event.pos[0], event.pos[1],
                        event.rel[0], event.rel[1],
                    )
                else:
                    self._mouse_position_event_func(
                        event.pos[0], event.pos[1],
                        event.rel[0], event.rel[1],
                    )

            elif event.type == pygame.MOUSEBUTTONDOWN:
                button = self._mouse_button_map.get(event.button, None)
                if button is not None:
                    self._handle_mouse_button_state_change(button, True)
                    self._mouse_release_event_func(
                        event.pos[0], event.pos[1],
                        button,
                    )

            elif event.type == pygame.MOUSEBUTTONUP:
                button = self._mouse_button_map.get(event.button, None)
                if button is not None:
                    self._handle_mouse_button_state_change(button, False)
                    self._mouse_press_event_func(
                        event.pos[0], event.pos[1],
                        button,
                    )

            elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                self._handle_mods()

                if event.key == pygame.K_ESCAPE:
                    self.close()

                if event.type == pygame.KEYDOWN:
                    self._key_pressed_map[event.key] = True
                elif event.type == pygame.KEYUP:
                    self._key_pressed_map[event.key] = False

                self._key_event_func(event.key, event.type, self._modifiers)

            elif event.type == pygame.TEXTINPUT:
                self._unicode_char_entered_func(event.text)

            elif event.type == pygame.MOUSEWHEEL:
                self._mouse_scroll_event_func(float(event.wheel.x), float(event.wheel.y))

            elif event.type == pygame.QUIT:
                self.close()

            elif event.type == pygame.VIDEORESIZE:
                self.resize(event.size[0], event.size[1])

            elif event.type == pygame.ACTIVEEVENT:
                print('ACTIVEEVENT', event)
                # gain 0/1: mouse inside or outside window
                pass

            elif event.type == pygame.WINDOWEVENT:
                if event.window.event == pygame.WINDOWEVENT_MINIMIZED:
                    self._iconify_func(True)
                elif event.window.event == pygame.WINDOWEVENT_RESTORED:
                    self._iconify_func(False)
            else:
                print('****', event)

    def destroy(self) -> None:
        """Gracefully close the window"""
        pygame.quit()
