from unittest import TestCase
from moderngl_window.conf import Settings

class SettingsTests(TestCase):
    """Test settings system"""
    # Non-standard window settings
    window_setting = {
        'class': 'moderngl_window.context.headless.Window',
        'name': 'ModernGL Headless Test',
        'gl_version': (3, 3),
    }

    def test_default(self):
        """Initialize default settings"""
        settings = Settings()
        # Attempt to access default properties
        settings.WINDOW
        settings.PROGRAM_FINDERS
        settings.PROGRAM_DIRS
        settings.PROGRAM_LOADERS

    def test_apply_dict(self):
        """Supply config values as dict"""
        settings = Settings()
        settings.setup(WINDOW=self.window_setting)
        self.assertEqual(settings.WINDOW, self.window_setting)

    def test_apply_cls(self):
        """Supply config values using cls namespace"""
        class MyConfig:
            WINDOW=self.window_setting

        settings = Settings()
        settings.setup(settings_cls=MyConfig)
        self.assertEqual(settings.WINDOW, self.window_setting)
