"""
General helper functions aiding in the boostrapping of this library.
"""
# pylint: disable = redefined-outer-name, too-few-public-methods
import argparse
import logging
import os
import sys

from pathlib import Path
from typing import List, Type

import moderngl
from moderngl_window.context.base import WindowConfig, BaseWindow
from moderngl_window.timers.clock import Timer
from moderngl_window.conf import settings
from moderngl_window.utils.module_loading import import_string

__version__ = "2.3.0"

IGNORE_DIRS = [
    "__pycache__",
    "base",
]

# Add new windows classes here to be recognized by the command line option --window
WINDOW_CLASSES = ["glfw", "headless", "pygame2", "pyglet", "pyqt5", "pyside2", "sdl2", "tk"]

OPTIONS_TRUE = ["yes", "on", "true", "t", "y", "1"]
OPTIONS_FALSE = ["no", "off", "false", "f", "n", "0"]
OPTIONS_ALL = OPTIONS_TRUE + OPTIONS_FALSE

# Quick and dirty debug logging setup by default
# See: https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial
logger = logging.getLogger(__name__)


def setup_basic_logging(level: int):
    """Set up basic logging

    Args:
        level (int): The log level
    """
    if level is None:
        return

    # Do not add a new handler if we already have one
    if not logger.handlers:
        logger.propagate = False
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(ch)


class ContextRefs:
    """Namespace for window/context references"""

    WINDOW = None
    CONTEXT = None


def activate_context(window: BaseWindow = None, ctx: moderngl.Context = None):
    """
    Register the active window and context.
    If only a window is supplied the context is taken from the window.
    Only a context can also be passed in.

    Keyword Args:
        window (window): The window to activate
        ctx (moderngl.Context): The moderngl context to activate
    """
    ContextRefs.WINDOW = window
    ContextRefs.CONTEXT = ctx
    if not ctx:
        ContextRefs.CONTEXT = window.ctx


def window():
    """Obtain the active window"""
    if ContextRefs.WINDOW:
        return ContextRefs.WINDOW

    raise ValueError("No active window and context. Call activate_window.")


def ctx():
    """Obtain the active context"""
    if ContextRefs.CONTEXT:
        return ContextRefs.CONTEXT

    raise ValueError("No active window and context. Call activate_window.")


def get_window_cls(window: str = None) -> Type[BaseWindow]:
    """
    Attempt to obtain a window class using the full dotted
    python path. This can be used to import custom or modified
    window classes.

    Args:
        window (str): Name of the window

    Returns:
        A reference to the requested window class. Raises exception if not found.
    """
    logger.info("Attempting to load window class: %s", window)
    return import_string(window)


def get_local_window_cls(window: str = None) -> Type[BaseWindow]:
    """
    Attempt to obtain a window class in the moderngl_window package
    using short window names such as ``pyglet`` or ``glfw``.

    Args:
        window (str): Name of the window

    Returns:
        A reference to the requested window class. Raises exception if not found.
    """
    window = os.environ.get("MODERNGL_WINDOW") or window
    if not window:
        window = "pyglet"

    return get_window_cls("moderngl_window.context.{}.Window".format(window))


def find_window_classes() -> List[str]:
    """
    Find available window packages
    Returns:
        A list of available window packages
    """
    # In some environments we cannot rely on introspection
    # and instead return a hardcoded list
    try:
        return [
            path.parts[-1]
            for path in Path(__file__).parent.joinpath("context").iterdir()
            if path.is_dir() and path.parts[-1] not in IGNORE_DIRS
        ]
    except Exception:
        return WINDOW_CLASSES


def create_window_from_settings() -> BaseWindow:
    """
    Creates a window using configured values in :py:attr:`moderngl_window.conf.Settings.WINDOW`.
    This will also activate the window/context.

    Returns:
        The Window instance
    """
    window_cls = import_string(settings.WINDOW["class"])
    window = window_cls(**settings.WINDOW)
    activate_context(window=window)
    return window


# --- The simple window config system ---


def run_window_config(config_cls: WindowConfig, timer=None, args=None) -> None:
    """
    Run an WindowConfig entering a blocking main loop

    Args:
        config_cls: The WindowConfig class to render
    Keyword Args:
        timer: A custom timer instance
        args: Override sys.args
    """
    setup_basic_logging(config_cls.log_level)
    parser = create_parser()
    config_cls.add_arguments(parser)
    values = parse_args(args=args, parser=parser)
    config_cls.argv = values
    window_cls = get_local_window_cls(values.window)

    # Calculate window size
    size = values.size or config_cls.window_size
    size = int(size[0] * values.size_mult), int(size[1] * values.size_mult)

    # Resolve cursor
    show_cursor = values.cursor
    if show_cursor is None:
        show_cursor = config_cls.cursor

    window = window_cls(
        title=config_cls.title,
        size=size,
        fullscreen=config_cls.fullscreen or values.fullscreen,
        resizable=values.resizable
        if values.resizable is not None
        else config_cls.resizable,
        gl_version=config_cls.gl_version,
        aspect_ratio=config_cls.aspect_ratio,
        vsync=values.vsync if values.vsync is not None else config_cls.vsync,
        samples=values.samples if values.samples is not None else config_cls.samples,
        cursor=show_cursor if show_cursor is not None else True,
    )
    window.print_context_info()
    activate_context(window=window)
    timer = timer or Timer()
    window.config = config_cls(ctx=window.ctx, wnd=window, timer=timer)

    # Swap buffers once before staring the main loop.
    # This can trigged additional resize events reporting
    # a more accurate buffer size
    window.swap_buffers()
    window.set_default_viewport()

    timer.start()

    while not window.is_closing:
        current_time, delta = timer.next_frame()

        if window.config.clear_color is not None:
            window.clear(*window.config.clear_color)

        # Always bind the window framebuffer before calling render
        window.use()

        window.render(current_time, delta)
        if not window.is_closing:
            window.swap_buffers()

    _, duration = timer.stop()
    window.destroy()
    if duration > 0:
        logger.info(
            "Duration: {0:.2f}s @ {1:.2f} FPS".format(
                duration, window.frames / duration
            )
        )


def create_parser():
    """Create an argparser parsing the standard arguments for WindowConfig"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-wnd",
        "--window",
        choices=find_window_classes(),
        help="Name for the window type to use",
    )
    parser.add_argument(
        "-fs",
        "--fullscreen",
        action="store_true",
        help="Open the window in fullscreen mode",
    )
    parser.add_argument(
        "-vs", "--vsync", type=valid_bool, help="Enable or disable vsync",
    )
    parser.add_argument(
        "-r",
        "--resizable",
        type=valid_bool,
        default=None,
        help="Enable/disable window resize",
    )
    parser.add_argument(
        "-s",
        "--samples",
        type=int,
        help="Specify the desired number of samples to use for multisampling",
    )
    parser.add_argument(
        "-c",
        "--cursor",
        type=valid_bool,
        help="Enable or disable displaying the mouse cursor",
    )
    parser.add_argument(
        "--size", type=valid_window_size, help="Window size",
    )
    parser.add_argument(
        "--size_mult",
        type=valid_window_size_multiplier,
        default=1.0,
        help="Multiplier for the window size making it easy scale the window",
    )
    return parser


def parse_args(args=None, parser=None):
    """Parse arguments from sys.argv

    Passing in your own argparser can be user to extend the parser.

    Keyword Args:
        args: override for sys.argv
        parser: Supply your own argparser instance
    """
    parser = parser or create_parser()
    return parser.parse_args(args or sys.argv[1:])


# --- Validators ---


def valid_bool(value):
    """Validator for bool values"""
    value = value.lower()
    if value is None:
        return None

    if value in OPTIONS_TRUE:
        return True

    if value in OPTIONS_FALSE:
        return False

    raise argparse.ArgumentTypeError(
        "Boolean value expected. Options: {}".format(OPTIONS_ALL)
    )


def valid_window_size(value):
    """
    Validator for window size parameter.

    Valid format is "[int]x[int]". For example "1920x1080".
    """
    try:
        width, height = value.split("x")
        return int(width), int(height)
    except ValueError:
        pass

    raise argparse.ArgumentTypeError(
        "Valid size format: int]x[int]. Example '1920x1080'",
    )


def valid_window_size_multiplier(value):
    """Validates window size multiplier

    Must be an integer or float greater than 0
    """
    try:
        val = float(value)
        if val > 0:
            return val
    except ValueError:
        pass

    raise argparse.ArgumentTypeError("Must be a positive int or float",)
