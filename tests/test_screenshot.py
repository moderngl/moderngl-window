from pathlib import Path
from unittest import mock

from headless import HeadlessTestCase
from utils import settings_context

from moderngl_window import screenshot


class ScreenshotTestCase(HeadlessTestCase):

    @mock.patch('PIL.Image.Image.save', new=mock.MagicMock())
    def test_fbo(self):
        """Create screenshot from fbo"""
        screenshot.create(self.window.fbo)

    @mock.patch('PIL.Image.Image.save', new=mock.MagicMock())
    def test_texture(self):
        """Create screenshot from texture"""
        texture = self.ctx.texture((16, 16), 4)
        screenshot.create(texture)

    @mock.patch('os.makedirs', new=mock.MagicMock())
    def test_with_screenshot_path(self):
        """Create screenshot with SCREENSHOT_PATH defined in settings"""
        with settings_context({'SCREENSHOT_PATH': (Path.cwd() / 'screenshots')}):
            self.test_fbo()

    def test_incorrect_source(self):
        """Attempt to pass invalid source"""
        with self.assertRaises(ValueError):
            screenshot.create("Hello")
