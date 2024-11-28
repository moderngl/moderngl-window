import os
import sys
from types import ModuleType
from unittest import TestCase

from moderngl_window.conf import SETTINGS_ENV_VAR, Settings
from moderngl_window.exceptions import ImproperlyConfigured


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

    def test_apply_settings_from_env(self):
        """Config values from module"""
        # Create and inject a fake module in python
        module_name = "moderngl_window_settings_module"
        module = ModuleType(module_name)
        setattr(module, 'WINDOW', self.window_setting)
        sys.modules[module_name] = module

        # Attempt to import it
        os.environ[SETTINGS_ENV_VAR] = module_name
        settings = Settings()
        settings.apply_settings_from_env()
        self.assertEqual(settings.WINDOW, self.window_setting)

    def test_import_nonexistent_module(self):
        """Import settings module that do no exist"""
        os.environ[SETTINGS_ENV_VAR] = 'this.module.does.not.exist'
        with self.assertRaises(ImproperlyConfigured):
            Settings().apply_settings_from_env()

    def test_apply_from_dict(self):
        """Supply config values as dict"""
        settings = Settings()
        settings.apply_from_dict({'WINDOW': self.window_setting})
        self.assertEqual(settings.WINDOW, self.window_setting)

    def test_apply_from_cls(self):
        """Supply config values using cls namespace"""
        class MyConfig:
            WINDOW=self.window_setting

        settings = Settings()
        settings.apply_from_cls(MyConfig)
        self.assertEqual(settings.WINDOW, self.window_setting)

    def test_apply_from_generator(self):
        """Test generators specifically"""
        def gen():
            yield 'WINDOW', self.window_setting
            yield 'SOMETHING', 1

        settings = Settings()
        settings.apply_from_iterable(gen())
        self.assertEqual(settings.WINDOW, self.window_setting)
        self.assertEqual(settings.SOMETHING, 1)

    def test_apply_from_iterator_error(self):
        """Ensure ValueError is rasied if not iterable"""
        with self.assertRaises(ValueError):
            settings = Settings()
            settings.apply_from_iterable(1337)

    def test_repr(self):
        """Ensure string represenation is somewhat reasonable"""
        value = str(Settings())
        self.assertIsInstance(value, str)
        self.assertGreater(len(value), 100)
