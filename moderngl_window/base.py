import sys
from typing import Any, Tuple

import moderngl


class BaseKeys:
    """
    Namespace for mapping key constants.
    This is simply a template for what keys should be mapped for all window libraries
    """
    # Fallback press/release action when window libraries don't have this
    ACTION_PRESS = 'ACTION_PRESS'
    ACTION_RELEASE = 'ACTION_RELEASE'

    ESCAPE = None
    SPACE = None
    ENTER = None
    PAGE_UP = None
    PAGE_DOWN = None
    LEFT = None
    RIGHT = None
    UP = None
    DOWN = None

    A = None
    B = None
    C = None
    D = None
    E = None
    F = None
    G = None
    H = None
    I = None
    J = None
    K = None
    L = None
    M = None
    N = None
    O = None
    P = None
    Q = None
    R = None
    S = None
    T = None
    U = None
    V = None
    W = None
    X = None
    Y = None
    Z = None


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

        self.ctx = None  # type: moderngl.Context
        self.example = None  # type: Example
        self.frames = 0  # Frame counter
        self._close = False

        if not self.keys:
            raise ValueError("Window {} class missing keys".format(self.__class__))

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

    def close(self):
        """
        Signal for the window to close
        """
        self._close = True

    def render(self, time: float, frame_time: float):
        """
        Renders the assigned example

        Args:
            time (float): Current time in seconds
            frame_time (float): Delta time from last frame in seconds
        """
        self.example.render(time, frame_time)

    def swap_buffers(self):
        """
        A library specific buffer swap method is required
        """
        raise NotImplementedError()

    def resize(self, width, height):
        """
        Should be called every time window is resized
        so the example can adapt to the new size if needed
        """
        if self.example:
            self.example.resize(width, height)

    def destroy(self):
        """
        A library specific destroy method is required
        """
        raise NotImplementedError()

    def set_default_viewport(self):
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


class Example:
    """
    Base class for making an example.
    Examples can be rendered by any supported window library and platform.
    """
    window_size = (1280, 720)
    resizable = True
    gl_version = (3, 3)
    title = "Example"
    aspect_ratio = 16 / 9

    def __init__(self, ctx=None, wnd=None, **kwargs):
        self.ctx = ctx
        self.wnd = wnd

    def render(self, time: float, frame_time: float):
        """
        Renders the assigned effect

        Args:
            time (float): Current time in seconds
            frame_time (float): Delta time from last frame in seconds
        """
        raise NotImplementedError("Example:render not implemented")

    def resize(self, width: int, height: int):
        """
        Called every time the window is resized
        in case the example needs to do internal adjustments.

        Width and height are reported in buffer size (not window size)
        """
        pass

    def key_event(self, key: Any, action: Any):
        """
        Called for every key press and release

        Args:
            key (int): The key that was press. Compare with self.wnd.keys.
            action: self.wnd.keys.ACTION_PRESS or ACTION_RELEASE
        """
        pass

    def mouse_position_event(self, x: int, y: int):
        """
        Reports the current mouse cursor position in the window

        Args:
            x (int): X postion of the mouse cursor
            y Iint): Y position of the mouse cursor
        """
        pass

    def mouse_press_event(self, x: int, y: int, button: int):
        """
        Called when a mouse button in pressed

        Args:
            x (int): X position the press occured
            y (int): Y position the press occured
            button (int): 1 = Left button, 2 = right button
        """
        pass

    def mouse_release_event(self, x: int, y: int, button: int):
        """
        Called when a mouse button in released

        Args:
            x (int): X position the release occured
            y (int): Y position the release occured
            button (int): 1 = Left button, 2 = right button
        """
        pass
