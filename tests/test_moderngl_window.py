import sys
from unittest import TestCase, mock

import moderngl

import moderngl_window as mglw
from moderngl_window.context.base import BaseWindow


def swap_buffers(self):
    """Swapbuffers closing window after 3 frames"""
    self._frames += 1
    if self._frames > 3:
        self.close()


class Config(mglw.WindowConfig):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, time: float, frame_time: float):
        pass


class ModernGlWindowTestCase(TestCase):

    @mock.patch('moderngl_window.context.headless.Window.swap_buffers', new=swap_buffers)
    def test_run_window_config(self):
        sys.argv = [
            'something',
            '-wnd', 'headless',
            '--size_mult', '1.0',
            '--cursor', 'False',
            '--size', '100x100',
        ]
        mglw.run_window_config(Config)

        self.assertIsInstance(mglw.window(), BaseWindow)
        self.assertIsInstance(mglw.ctx(), moderngl.Context)
