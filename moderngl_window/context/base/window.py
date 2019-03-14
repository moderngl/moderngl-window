from functools import wraps
import sys
from typing import Any, Tuple, Type

import moderngl
from moderngl_window.context.base import WindowConfig, KeyModifiers


def require_callable(func):
    """Decorator ensuring assigned callbacks are valid callables"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not callable(args[1]):
            raise ValueError("{} is not a callable".format(args[1]))
        return func(*args, **kwargs)
    return wrapper


class BaseWindow:
    """
    Helper base class for a generic window implementation
    """
    keys = None  # type: BaseKeys

    def __init__(self, title="Example", gl_version=(3, 3), size=(1280, 720), resizable=True,
                 fullscreen=False, vsync=True, aspect_ratio=16/9, samples=4, cursor=True,
                 create_mgl_context=True, **kwargs):
        """
        Args:
            title (str): The window title
            gl_version (tuple): Major and minor version of the opengl context to create
            size (tuple): Window size x, y
            resizable (bool): Should the window be resizable?
            fullscreen (bool): Open window in fullsceeen mode
            vsync (bool): Enable/disable vsync
            aspect_ratio (float): The desired aspect ratio. Can be set to None.
            samples (int): Number of MSAA samples for the default framebuffer
            cursor (bool): Enable/disable displaying the cursor inside the window
            create_mgl_context (bool): Auto create a ModernGL context
        """
        # Window parameters
        self._title = title
        self._gl_version = gl_version
        self._width, self._height = size
        self._resizable = resizable
        self._buffer_width, self._buffer_height = size
        self._fullscreen = fullscreen
        self._vsync = vsync
        self._aspect_ratio = aspect_ratio
        self._samples = samples
        self._cursor = cursor

        # Callback functions
        self._render_func = dummy_func
        self._resize_func = dummy_func
        self._key_event_func = dummy_func
        self._mouse_position_event_func = dummy_func
        self._mouse_press_event_func = dummy_func
        self._mouse_release_event_func = dummy_func

        # Internal states
        self._ctx = None  # type: moderngl.Context
        self._viewport = None
        self._frames = 0  # Frame counter
        self._close = False
        self._config = None
        self._create_mgl_context = create_mgl_context
        self._key_pressed_map = {}
        self._modifiers = KeyModifiers

        # Do not allow resize in fullscreen
        if self.fullscreen:
            self.resizable = False

        if not self.keys:
            raise ValueError("Window class {} missing keys attribute".format(self.__class__))

    def init_mgl_context(self, ctx=None) -> None:
        """
        Create or assign a ModernGL context. If no context is supplied a context will be
        created using the window's gl_version.

        Keyword Args:
            ctx: An optional custom ModernGL context
        """
        if self._ctx:
            raise ValueError("A ModernGL context is already assigned")

        self._ctx = ctx or moderngl.create_context(require=self.gl_version_code)

    @property
    def ctx(self) -> moderngl.Context:
        """moderngl.Context: The ModernGL context for the window"""
        return self._ctx

    @property
    def title(self) -> str:
        """str: Window title"""
        return self._title

    @property
    def gl_version(self) -> Tuple[int, int]:
        """(major, minor): Required OpenGL version"""
        return self._gl_version

    @property
    def width(self) -> int:
        """int: The current window width"""
        return self._width
    
    @property
    def height(self) -> int:
        """int: The current window height"""
        return self._height

    @property
    def size(self) -> Tuple[int, int]:
        """
        (width, height): current window size
        """
        return self._width, self._height

    @property
    def buffer_size(self) -> Tuple[int, int]:
        """
        Returns: (with, heigh) tuple with the current window buffer size
        """
        return self._buffer_width, self._buffer_height

    @property
    def viewport(self) -> Tuple[int, int, int, int]:
        """(int, int, int, int): current window viewport"""
        return self._viewport

    @property
    def frames(self) -> int:
        """int: Number of frames rendered"""
        return self._frames

    @property
    def resizable(self) -> bool:
        """bool: Window is resizable"""
        return self._resizable

    @property
    def fullscreen(self) -> bool:
        """bool: Window is in fullscreen mode"""
        return self._fullscreen

    @property
    def config(self) -> WindowConfig:
        """Get the current WindowConfig instance"""
        return self._config

    @property
    def vsync(self) -> bool:
        """bool: vertical sync enabled/disabled"""
        return self._vsync

    @property
    def aspect_ratio(self) -> float:
        """float: Aspect ratio configured for the viewport"""
        return self._aspect_ratio

    @property
    def samples(self) -> float:
        """float: Number of Multisample anti-aliasing (MSAA) samples"""
        return self._samples

    @property
    def cursor(self) -> bool:
        return self._cursor

    @config.setter
    def config(self, config) -> None:
        """
        Set up the WindowConfig instance.
        A WindowConfig class is not required, but callback methods must be mapped.
        """
        self.render_func = getattr(config, 'render', dummy_func)
        self.resize_func = getattr(config, 'resize', dummy_func)
        self.key_event_func = getattr(config, 'key_event', dummy_func)
        self.mouse_position_event_func = getattr(config, 'mouse_position_event', dummy_func)
        self.mouse_press_event_func = getattr(config, 'mouse_press_event', dummy_func)
        self.mouse_release_event_func = getattr(config, 'mouse_release_event', dummy_func)

        self._config = config

    @property
    def render_func(self):
        return self._render_func

    @render_func.setter
    @require_callable
    def render_func(self, func):
        self._render_func = func

    @property
    def resize_func(self):
        return self._resize_func

    @resize_func.setter
    @require_callable
    def resize_func(self, func):
        self._resize_func = func

    @property
    def key_event_func(self):
        return self._key_event_func

    @key_event_func.setter
    @require_callable
    def key_event_func(self, func):
        self._key_event_func = func

    @property
    def mouse_position_event_func(self):
        return self._mouse_position_event_func

    @mouse_position_event_func.setter
    @require_callable
    def mouse_position_event_func(self, func):
        self._mouse_position_event_func = func

    @property
    def mouse_press_event_func(self):
        return self._mouse_press_event_func

    @mouse_press_event_func.setter
    @require_callable
    def mouse_press_event_func(self, func):
        self._mouse_press_event_func = func

    @property
    def mouse_release_event_func(self):
        return self._mouse_release_event_func

    @mouse_release_event_func.setter
    @require_callable
    def mouse_release_event_func(self, func):
        self._mouse_release_event_func = func

    @property
    def modifiers(self) -> Type[KeyModifiers]:
        """(KeyModifiers) The current keyboard modifiers"""
        return self._modifiers

    def is_key_pressed(self, key) -> bool:
        """Returns: The press state of a key"""
        return self._key_pressed_map.get(key) == True

    @property
    def is_closing(self) -> bool:
        """bool: Is the window about to close?"""
        return self._close

    def close(self) -> None:
        """Signal for the window to close"""
        self._close = True

    def render(self, time: float, frame_time: float) -> None:
        """
        Renders a frame by calling the configured render callback

        Args:
            time (float): Current time in seconds
            frame_time (float): Delta time from last frame in seconds
        """
        self.render_func(time, frame_time)

    def swap_buffers(self) -> None:
        """
        Library specific buffer swap method. Must be overridden.
        """
        raise NotImplementedError()

    def resize(self, width, height) -> None:
        """
        Should be called every time window is resized
        so the example can adapt to the new size if needed
        """
        if self._resize_func:
            self._resize_func(width, height)

    def destroy(self) -> None:
        """
        A library specific destroy method is required
        """
        raise NotImplementedError()

    def set_default_viewport(self) -> None:
        """
        Calculates the viewport based on the configured aspect ratio.
        Will add black borders and center the viewport if the window
        do not match the configured viewport.

        If aspect ratio is None the viewport will be scaled
        to the entire window size regardless of size.
        """
        if self._aspect_ratio:
            expected_width = int(self._buffer_height * self._aspect_ratio)
            expected_height = int(expected_width / self._aspect_ratio)

            if expected_width > self._buffer_width:
                expected_width = self._buffer_width
                expected_height =  int(expected_width / self._aspect_ratio)

            blank_space_x = self._buffer_width - expected_width
            blank_space_y = self._buffer_height - expected_height

            self._viewport = (
                blank_space_x // 2,
                blank_space_y // 2,
                expected_width,
                expected_height,
            )
        else:
            self._viewport = (0, 0, self._buffer_width, self._buffer_height)

        self._ctx.viewport = self._viewport

    @property
    def gl_version_code(self) -> int:
        """
        Generates the version code integer for the selected OpenGL version.
        Example: gl_version (4, 1) returns 410
        """
        return self.gl_version[0] * 100 +  self.gl_version[1] * 10

    def print_context_info(self):
        """
        Prints moderngl context info.
        """
        print("Context Version:")
        print('ModernGL:', moderngl.__version__)
        print('vendor:', self._ctx.info['GL_VENDOR'])
        print('renderer:', self._ctx.info['GL_RENDERER'])
        print('version:', self._ctx.info['GL_VERSION'])
        print('python:', sys.version)
        print('platform:', sys.platform)
        print('code:', self._ctx.version_code)


def dummy_func(*args, **kwargs) -> None:
    """Dummy function used as the default for callbacks"""
    pass
