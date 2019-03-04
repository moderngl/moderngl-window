import sys
from typing import Any, Tuple

import moderngl
from moderngl_window.base import WindowConfig


class BaseWindow:
    """
    Helper base class for a generic window implementation
    """
    keys = None  # type: BaseKeys

    def __init__(self, title="Example", gl_version=(3, 3), size=(1280, 720), resizable=True,
                 fullscreen=False, vsync=True, aspect_ratio=16/9, samples=4, cursor=True, **kwargs):
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
        """
        # Window parameters
        self.title = title
        self.gl_version = gl_version
        self.width, self.height = size
        self.resizable = resizable
        self.buffer_width, self.buffer_height = size
        self.fullscreen = fullscreen
        self.vsync = vsync
        self.aspect_ratio = aspect_ratio
        self.samples = samples
        self.cursor = cursor

        # Callback functions
        self.render_func = dummy_func
        self.resize_func = dummy_func
        self.key_event_func = dummy_func
        self.mouse_position_event_func = dummy_func
        self.mouse_press_event_func = dummy_func
        self.mouse_release_event_func = dummy_func

        # Internal states
        self.ctx = None  # type: moderngl.Context
        self.frames = 0  # Frame counter
        self._close = False
        self._config = None

        if not self.keys:
            raise ValueError("Window {} class missing keys".format(self.__class__))

    @property
    def config(self) -> WindowConfig:
        """Get the current WindowConfig instance"""
        return self._config

    @config.setter
    def config(self, config):
        """Set up the WindowConfig instance"""
        self.render_func = getattr(config, 'render', dummy_func)
        self.resize_func = getattr(config, 'resize', dummy_func)
        self.key_event_func = getattr(config, 'key_event', dummy_func)
        self.mouse_position_event_func = getattr(config, 'mouse_position_event', dummy_func)
        self.mouse_press_event_func = getattr(config, 'mouse_press_event', dummy_func)
        self.mouse_release_event_func = getattr(config, 'mouse_release_event', dummy_func)

        self._config = config

    @property
    def size(self) -> Tuple[int, int]:
        """
        Returns: (width, height) tuple with the current window size
        """
        return self.width, self.height

    @property
    def buffer_size(self) -> Tuple[int, int]:
        """
        Returns: (with, heigh) tuple with the current window buffer size
        """
        return self.buffer_width, self.buffer_height

    @property
    def is_closing(self) -> bool:
        """
        Returns: (bool) Is the window about to close?
        """
        return self._close

    def close(self) -> None:
        """
        Signal for the window to close
        """
        self._close = True

    def render(self, time: float, frame_time: float) -> None:
        """
        Renders a frame

        Args:
            time (float): Current time in seconds
            frame_time (float): Delta time from last frame in seconds
        """
        self.render_func(time, frame_time)

    def swap_buffers(self) -> None:
        """
        Library specific buffer swap method
        """
        raise NotImplementedError()

    def resize(self, width, height) -> None:
        """
        Should be called every time window is resized
        so the example can adapt to the new size if needed
        """
        if self.config:
            self.config.resize(width, height)

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
        if self.aspect_ratio:
            expected_width = int(self.buffer_height * self.aspect_ratio)
            expected_height = int(expected_width / self.aspect_ratio)

            if expected_width > self.buffer_width:
                expected_width = self.buffer_width
                expected_height =  int(expected_width / self.aspect_ratio)

            blank_space_x = self.buffer_width - expected_width
            blank_space_y = self.buffer_height - expected_height

            self.ctx.viewport = (
                blank_space_x // 2,
                blank_space_y // 2,
                expected_width,
                expected_height,
            )
        else:
            self.ctx.viewport = (0, 0, self.buffer_width, self.buffer_height)

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
        print('vendor:', self.ctx.info['GL_VENDOR'])
        print('renderer:', self.ctx.info['GL_RENDERER'])
        print('version:', self.ctx.info['GL_VERSION'])
        print('python:', sys.version)
        print('platform:', sys.platform)
        print('code:', self.ctx.version_code)


def dummy_func(*args, **kwargs) -> None:
    """Dummy function used as the default for callbacks"""
    pass
