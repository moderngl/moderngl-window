from unittest import TestCase

import moderngl
import moderngl_window
from moderngl_window.conf import settings


class HeadlessTestCase(TestCase):
    """Test using a headless window/context"""
    window_size = (16, 16)
    aspect_ratio = 1.0

    @classmethod
    def setUpClass(cls):
        """Create a headless window and activate the context"""
        settings.WINDOW['class'] = 'moderngl_window.context.headless.Window'
        settings.WINDOW['size'] = cls.window_size
        settings.WINDOW['aspect_ratio'] = cls.aspect_ratio

        cls.window = moderngl_window.create_window_from_settings()
        moderngl_window.activate_context(window=cls.window)

    @property
    def ctx(self) -> moderngl.Context:
        """moderngl.Context: The active context"""
        return moderngl_window.ctx()
