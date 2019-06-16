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
