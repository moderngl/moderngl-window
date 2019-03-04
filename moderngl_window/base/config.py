from typing import Any, Tuple


class WindowConfig:
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
