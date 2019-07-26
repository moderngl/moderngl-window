from unittest import mock
from headless import HeadlessTestCase

from moderngl_window import screenshot


class ScreenshotTestCase(HeadlessTestCase):

    @mock.patch('PIL.Image.Image.save', new=mock.MagicMock())
    def test_create_fbo(self):
        """Create screenshot from fbo"""
        screenshot.create(self.window.fbo)

    @mock.patch('PIL.Image.Image.save', new=mock.MagicMock())
    def test_create_texture(self):
        """Create screenshot from texture"""        
        texture = self.ctx.texture((16, 16), 4)
        screenshot.create(texture)
