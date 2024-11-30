from ctypes import c_char_p, c_int
from pathlib import Path
from typing import Any

import sdl2
import sdl2.ext
import sdl2.video

from moderngl_window.context.base import BaseWindow
from moderngl_window.context.sdl2.keys import Keys


class Window(BaseWindow):
    """
    Basic window implementation using SDL2.
    """

    #: Name of the window
    name = "sdl2"
    #: SDL2 specific key constants
    keys = Keys

    _mouse_button_map = {
        1: 1,
        3: 2,
        2: 3,
    }

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            raise ValueError("Failed to initialize sdl2")

        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, self.gl_version[0])
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, self.gl_version[1])
        sdl2.video.SDL_GL_SetAttribute(
            sdl2.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.SDL_GL_CONTEXT_PROFILE_CORE
        )
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, 1)
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)
        sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_STENCIL_SIZE, 8)

        self.cursor = self._cursor

        if self.samples > 1:
            sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLEBUFFERS, 1)
            sdl2.video.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLESAMPLES, self.samples)

        flags = sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_ALLOW_HIGHDPI
        if self.fullscreen:
            flags |= sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP
        else:
            if self.resizable:
                flags |= sdl2.SDL_WINDOW_RESIZABLE

        if not self._visible:
            flags |= sdl2.SDL_WINDOW_HIDDEN

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
        self._buffer_width, self._buffer_height = self._get_drawable_size()

        self.init_mgl_context()
        self.set_default_viewport()

    def _set_fullscreen(self, value: bool) -> None:
        sdl2.SDL_SetWindowFullscreen(
            self._window, sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP if value else 0
        )

    def _set_vsync(self, value: bool) -> None:
        sdl2.video.SDL_GL_SetSwapInterval(1 if value else 0)

    def _get_drawable_size(self) -> tuple[int, int]:
        x = c_int()
        y = c_int()
        sdl2.video.SDL_GL_GetDrawableSize(self._window, x, y)
        return x.value, y.value

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
        sdl2.SDL_SetWindowSize(self._window, value[0], value[1])
        # SDL_SetWindowSize don't trigger a resize event
        self.resize(value[0], value[1])

    @property
    def position(self) -> tuple[int, int]:
        """tuple[int, int]: The current window position.

        This property can also be set to move the window::

            # Move window to 100, 100
            window.position = 100, 100
        """
        x = c_int(0)
        y = c_int(0)
        sdl2.SDL_GetWindowPosition(self._window, x, y)
        return x.value, y.value

    @position.setter
    def position(self, value: tuple[int, int]) -> None:
        sdl2.SDL_SetWindowPosition(self._window, value[0], value[1])

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
            sdl2.SDL_ShowWindow(self._window)
        else:
            sdl2.SDL_HideWindow(self._window)

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
        sdl2.SDL_ShowCursor(sdl2.SDL_ENABLE if value else sdl2.SDL_DISABLE)
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
        if value is True:
            sdl2.SDL_SetRelativeMouseMode(sdl2.SDL_TRUE)
        else:
            sdl2.SDL_SetRelativeMouseMode(sdl2.SDL_FALSE)

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
        data = c_char_p(value.encode())
        sdl2.SDL_SetWindowTitle(self._window, data)
        self._title = value

    def swap_buffers(self) -> None:
        """Swap buffers, set viewport, trigger events and increment frame counter"""
        sdl2.SDL_GL_SwapWindow(self._window)
        self.set_default_viewport()
        self.process_events()
        self._frames += 1

    def resize(self, width: int, height: int) -> None:
        """Resize callback.

        Args:
            width: New window width
            height: New window height
        """
        self._width = width
        self._height = height
        self._buffer_width, self._buffer_height = self._get_drawable_size()
        self.set_default_viewport()

        super().resize(self._buffer_width, self._buffer_height)

    def _handle_mods(self) -> None:
        """Update key mods"""
        mods = sdl2.SDL_GetModState()
        self._modifiers.shift = mods & sdl2.KMOD_SHIFT
        self._modifiers.ctrl = mods & sdl2.KMOD_CTRL
        self._modifiers.alt = mods & sdl2.KMOD_ALT

    def _set_icon(self, icon_path: Path) -> None:
        sdl2.SDL_SetWindowIcon(self._window, sdl2.ext.load_image(icon_path))

    def process_events(self) -> None:
        """Handle all queued events in sdl2 dispatching events to standard methods"""
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_MOUSEMOTION:
                if self.mouse_states.any:
                    self._mouse_drag_event_func(
                        event.motion.x,
                        event.motion.y,
                        event.motion.xrel,
                        event.motion.yrel,
                    )
                else:
                    self._mouse_position_event_func(
                        event.motion.x,
                        event.motion.y,
                        event.motion.xrel,
                        event.motion.yrel,
                    )

            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                self._handle_mods()
                button = self._mouse_button_map.get(event.button.button, None)
                if button is not None:
                    self._handle_mouse_button_state_change(button, True)
                    self._mouse_press_event_func(
                        event.motion.x,
                        event.motion.y,
                        button,
                    )

            elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                self._handle_mods()
                button = self._mouse_button_map.get(event.button.button, None)
                if button is not None:
                    self._handle_mouse_button_state_change(button, False)
                    self._mouse_release_event_func(
                        event.motion.x,
                        event.motion.y,
                        button,
                    )

            elif event.type in [sdl2.SDL_KEYDOWN, sdl2.SDL_KEYUP]:
                self._handle_mods()

                if self._exit_key is not None and event.key.keysym.sym == self._exit_key:
                    self.close()

                if (
                    self._fs_key is not None
                    and event.key.keysym.sym == self._fs_key
                    and event.type == sdl2.SDL_KEYDOWN
                ):
                    self.fullscreen = not self.fullscreen

                if event.type == sdl2.SDL_KEYDOWN:
                    self._key_pressed_map[event.key.keysym.sym] = True
                elif event.type == sdl2.SDL_KEYUP:
                    self._key_pressed_map[event.key.keysym.sym] = False

                self._key_event_func(event.key.keysym.sym, event.type, self._modifiers)

            elif event.type == sdl2.SDL_TEXTINPUT:
                self._unicode_char_entered_func(event.text.text.decode())

            elif event.type == sdl2.SDL_MOUSEWHEEL:
                self._handle_mods()
                self._mouse_scroll_event_func(float(event.wheel.x), float(event.wheel.y))

            elif event.type == sdl2.SDL_QUIT:
                self.close()

            elif event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event in [
                    sdl2.SDL_WINDOWEVENT_RESIZED,
                    sdl2.SDL_WINDOWEVENT_SIZE_CHANGED,
                ]:
                    self.resize(event.window.data1, event.window.data2)
                elif event.window.event == sdl2.SDL_WINDOWEVENT_MINIMIZED:
                    self._visible = False
                    self._iconify_func(True)
                elif event.window.event == sdl2.SDL_WINDOWEVENT_RESTORED:
                    self._visible = True
                    self._iconify_func(False)

    def close(self) -> None:
        """Close the window"""
        super().close()
        self._close_func()

    def destroy(self) -> None:
        """Gracefully close the window"""
        sdl2.SDL_GL_DeleteContext(self._context)
        sdl2.SDL_DestroyWindow(self._window)
        sdl2.SDL_Quit()
