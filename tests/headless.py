from unittest import TestCase

import moderngl_window
from moderngl_window.conf import settings


class HeadlessTestCase(TestCase):
    """Test using a headless window/context"""

    @classmethod
    def setUpClass(cls):
        """Create a headless window and activate the context"""
        settings.WINDOW['class'] = 'moderngl_window.context.headless.Window'
        cls.window = moderngl_window.create_window_from_settings()
        moderngl_window.activate_context(window=cls.window)
