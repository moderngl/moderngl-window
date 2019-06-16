"""
Bag of settings values
"""
import importlib
import os
from moderngl_window.conf import default
from moderngl_window.exceptions import ImproperlyConfigured

SETTINGS_ENV_VAR = "MODERNGL_WINDOW_SETTINGS_MODULE"

# pylint: disable=C0103


class Settings:
    SETTINGS_MODULE = None

    def __init__(self):
        """Initialize settins with default values"""
        self.apply_default_settings()

    def setup(self, setting_module=None, settings_module_name=None, **kwargs):
        """
        Apply settings values from various sources

        Keyword Args:
            settings_module (module): Reference to a settings module
            settings_module_name (str): Full pythonpath to a settings module
        """
        self.SETTINGS_MODULE = setting_module
        if not setting_module:
            settings_module = os.environ.get(SETTINGS_ENV_VAR)

        # Apply settings module of supplied
        self.SETTINGS_MODULE = settings_module
        module = importlib.import_module(self.SETTINGS_MODULE)
        if not module:
            raise ImproperlyConfigured(
                "Settings module '{}' not found. ".format(self.SETTINGS_MODULE)
            )

        for setting in dir(module):
            if setting.isupper():
                value = getattr(module, setting)
                # TODO: Add more validation here
                setattr(self, setting, value)

    def update(self, **kwargs):
        """Override settings values"""
        for name, value in kwargs.items():
            setattr(self, name, value)

    def apply_default_settings(self):
        """Apply keys and values from the default settings module"""
        for setting in dir(default):
            if setting.isupper():
                setattr(self, setting, getattr(default, setting))

    def __repr__(self):
        return '<{cls} "{data}>"'.format(
            cls=self.__class__.__name__,
            data=None,
        )


settings = Settings()
