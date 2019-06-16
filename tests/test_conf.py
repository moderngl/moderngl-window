from unittest import TestCase
from moderngl_window.conf import Settings

class SettingsTests(TestCase):

    def test_default(self):
        settings = Settings()
