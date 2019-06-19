import argparse
import os
import sys
import time

from pathlib import Path
from typing import List, Type

import moderngl
from moderngl_window.context.base import WindowConfig, BaseWindow
from moderngl_window.timers.clock import Timer
from moderngl_window.conf import settings
from moderngl_window.utils.module_loading import import_string

IGNORE_DIRS = [
    '__pycache__',
    'base',
]

OPTIONS_TRUE = ['yes', 'on', 'true', 't', 'y', '1']
OPTIONS_FALSE = ['no', 'off', 'false', 'f', 'n', '0']
OPTIONS_ALL = OPTIONS_TRUE + OPTIONS_FALSE


class ContextRefs:
    WINDOW = None
    CONTEXT = None


def activate_context(window: BaseWindow = None, ctx: moderngl.Context = None):
    """
    Register the active window and context.
    If only a window is supplied the context is taken from the window.

    Keyword Args:
        window (window): The currenty active window
        ctx (moderngl.Context): The active moderngl context
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
    Attept to obtain a window class using the full dotted
    python path. This can be used to import custom or modified
    window classes.

    Args:
        window (str): Name of the window

    Returns:
        A reference to the requested window class. Raises exception if not found.
    """
    print("Attempting to load window class:", window)
    return import_string(window)


def get_local_window_cls(window: str = None) ->  Type[BaseWindow]:
    """
    Attept to obtain a window class in the moderngl_window package
    using short window names such as `pyqt5` or `glfw`.

    Args:
        window (str): Name of the window

    Returns:
        A reference to the requested window class. Raises exception if not found.
    """
    window = os.environ.get('MODERNGL_WINDOW') or window
    if not window:
        window = 'pyglet'

    return get_window_cls('moderngl_window.context.{}.Window'.format(window))


def find_window_classes() -> List[str]:
    """
    Find available window packages

    Returns:
        A list of avaialble window packages
    """
    return [
        path.parts[-1] for path in Path(__file__).parent.joinpath('context').iterdir()
        if path.is_dir() and path.parts[-1] not in IGNORE_DIRS
    ]


def create_window_from_settings() -> BaseWindow:
    """
    Creates a window using configured values in settings.WINDOW.
    This will also activate the window/context.

    Returns:
        The Window instance
    """
    window_cls = import_string(settings.WINDOW['class'])
    window = window_cls(**settings.WINDOW)
    activate_context(window=window)
    return window

# --- The simple window config system ---

def run_window_config(config_cls: WindowConfig, timer=None, args=None) -> None:
    """
    Run an WindowConfig entering a blocking main loop

    Args:
        config_cls: The WindowConfig class to render
        args: Override sys.args
    """
    values = parse_args(args)
    window_cls = get_local_window_cls(values.window)

    # Calculate window size
    size = values.size or config_cls.window_size
    size = int(size[0] * values.size_mult), int(size[1] * values.size_mult)

    window = window_cls(
        title=config_cls.title,
        size=size,
        fullscreen=values.fullscreen,
        resizable=config_cls.resizable,
        gl_version=config_cls.gl_version,
        aspect_ratio=config_cls.aspect_ratio,
        vsync=values.vsync,
        samples=values.samples,
        cursor=values.cursor,
    )
    window.print_context_info()
    activate_context(window=window)
    window.config = config_cls(ctx=window.ctx, wnd=window)

    timer = Timer()
    timer.start()

    while not window.is_closing:
        current_time, delta = timer.next_frame()

        window.use()
        window.clear()
        window.render(current_time, delta)
        window.swap_buffers()

    _, duration = timer.stop()
    window.destroy()
    print("Duration: {0:.2f}s @ {1:.2f} FPS".format(duration, window.frames / duration))


def parse_args(args=None):
    """Parse arguments from sys.argv"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-wnd', '--window',
        choices=find_window_classes(),
        help='Name for the window type to use',
    )
    parser.add_argument(
        '-fs', '--fullscreen',
        action="store_true",
        help='Open the window in fullscreen mode',
    )
    parser.add_argument(
        '-vs', '--vsync',
        type=valid_bool,
        default="1",
        help="Enable or disable vsync",
    )
    parser.add_argument(
        '-s', '--samples',
        type=int,
        default=4,
        help="Specify the desired number of samples to use for multisampling",
    )
    parser.add_argument(
        '-c', '--cursor',
        type=valid_bool,
        default="true",
        help="Enable or disable displaying the mouse cursor",
    )
    parser.add_argument(
        '--size',
        type=valid_window_size,
        help="Window size",
    )
    parser.add_argument(
        '--size_mult',
        type=valid_window_size_multiplier,
        default=1.0,
        help="Multiplier for the window size making it easy scale the window",
    )

    return parser.parse_args(args or sys.argv[1:])


# --- Validators ---

def valid_bool(value):
    """Validator for bool values"""
    value = value.lower()

    if value in OPTIONS_TRUE:
        return True

    if value in OPTIONS_FALSE:
        return False

    raise argparse.ArgumentTypeError('Boolean value expected. Options: {}'.format(OPTIONS_ALL))


def valid_window_size(value):
    """
    Validator for window size parameter.

    Valid format is "[int]x[int]". For example "1920x1080".
    """
    try:
        width, height = value.split('x')
        return int(width), int(height)
    except ValueError:
        pass

    raise argparse.ArgumentTypeError(
        "Valid size format: int]x[int]. Example '1920x1080'",
    )


def valid_window_size_multiplier(value):
    """
    Validates window size multiplier

    Must be an integer or float creater than 0
    """
    try:
        val = float(value)
        if val > 0:
            return val
    except ValueError:
        pass

    raise argparse.ArgumentTypeError(
        "Must be a positive int or float",
    )
