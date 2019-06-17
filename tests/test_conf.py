from unittest import TestCase
from moderngl_window.conf import Settings

class SettingsTests(TestCase):

    def test_default(self):
        """Initialize default settings"""
        settings = Settings()
        # Attempt to access default properties
        settings.WINDOW
        settings.PROGRAM_FINDERS
        settings.PROGRAM_DIRS
        settings.PROGRAM_LOADERS

    def test_apply_dict(self):
        window_data = {
            'class': 'moderngl_window.context.headless.Window',
            'name': 'ModernGL Headless Test',
            'gl_version': (3, 3),
        }
        settings = Settings()
        settings.setup(WINDOW=window_data)
        self.assertEqual(settings.WINDOW, window_data)
