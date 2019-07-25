"""
Bag of settings values
"""
# pylint: disable = invalid-name
import importlib
import types
import os

from collections.abc import Iterable
from pprint import pformat
from typing import Union


from moderngl_window.conf import default
from moderngl_window.exceptions import ImproperlyConfigured

SETTINGS_ENV_VAR = "MODERNGL_WINDOW_SETTINGS_MODULE"


class Settings:
    """
    Bag of settings values. New attributes can be freely added runtime.
    Various apply* methods are supplied so the user have full control over how
    settings values are initialized. This is especially useful for more custom usage.

    Attribute names must currently be in upper case to be recognized.

    Some examples of usage::

        from moderngl_window.conf import settings

        # Mandatory settings values
        try:
            value = settings.VALUE
        except KeyError:
            raise ValueError("This settings value is required")

        # Fallback in code
        value = getattr(settings, 'VALUE', 'default_value')

        # Pretty printed string represenation for easy inspection
        print(settings)
    """
    def __init__(self):
        """Initialize settings with default values"""
        # Set default entires. Mainly for code completion
        self.WINDOW = dict()
        self.SCREENSHOT_PATH = None
        # Finders
        self.PROGRAM_FINDERS = []
        self.TEXTURE_FINDERS = []
        self.SCENE_FINDERS = []
        self.DATA_FINDERS = []
        # Finder dirs
        self.PROGRAM_DIRS = []
        self.TEXTURE_DIRS = []
        self.SCENE_DIRS = []
        self.DATA_DIRS = []
        # Loaders
        self.PROGRAM_LOADERS = []
        self.TEXTURE_LOADERS = []
        self.SCENE_LOADERS = []
        self.DATA_LOADERS = []

        self.apply_default_settings()

    def apply_default_settings(self) -> None:
        """
        Apply keys and values from the default settings module
        located in this package. This is to ensure we always
        have the minimnal settings for the system to run.

        If replacing or customizing the settings class
        you must always apply default settings to ensure
        compatibility when new settings are added.
        """
        self.apply_from_module(default)

    def apply_settings_from_env(self) -> None:
        """
        Apply settings from MODERNGL_WINDOW_SETTINGS_MODULE environment variable.
        If the enviroment variable is undefined no action will be taken.
        Normally this would be used to easily be able to switch between
        different configuration by setting env vars before executing the program.

        Example::

            import os
            from moderngl_window.conf import settings

            os.environ['MODERNGL_WINDOW_SETTINGS_MODULE'] = 'python.path.to.module'
            settings.apply_settings_from_env()

        Raises:
            ImproperlyConfigured if the module was not found
        """
        name = os.environ.get(SETTINGS_ENV_VAR)
        if name:
            self.apply_from_module_name(name)

    def apply_from_module_name(self, settings_module_name: str) -> None:
        """
        Apply settings from a python module by supplying the full
        pythonpath to the module.

        Args:
            settings_module_name (str): Full python path to the module

        Raises:
            ImproperlyConfigured if the module was not found
        """
        try:
            module = importlib.import_module(settings_module_name)
        except ModuleNotFoundError as ex:
            raise ImproperlyConfigured(
                "Settings module '{}' not found. From importlib: {}".format(
                    settings_module_name,
                    ex,
                )
            )

        self.apply_from_module(module)

    def apply_from_dict(self, data: dict) -> None:
        """
        Apply settings values from a dictionary

        Example::

            >> from moderngl_window.conf import settings
            >> settings.apply_dict({'SOME_VALUE': 1})
            >> settings.SOME_VALUE
            1
        """
        self.apply_from_iterable(data.items())

    def apply_from_module(self, module: types.ModuleType) -> None:
        """
        Apply settings values from a python module

        Example::

            my_settings.py module containing the following line:
            SOME_VALUE = 1

            >> from moderngl_window.conf import settings
            >> import my_settings
            >> settings.apply_module(my_settings)
            >> settings.SOME_VALUE
            1
        """
        self.apply_from_iterable(module.__dict__.items())

    def apply_from_cls(self, cls) -> None:
        """
        Apply settings values from a class namespace

        Example::

            >> from moderngl_window.conf import settings
            >> class MySettings:
            >>    SOME_VALUE = 1
            >>
            >> settings.apply(MySettings)
            >> settings.SOME_VALUE
            1
        """
        self.apply_from_iterable(cls.__dict__.items())

    def apply_from_iterable(self, iterable: Union[Iterable, types.GeneratorType]) -> None:
        """
        Apply (key, value) pairs from an interable or generator
        """
        if not isinstance(iterable, Iterable) and not isinstance(self, types.GeneratorType):
            raise ValueError(
                "Input value is not a generator or interable, but of type: {}".format(type(iterable))
            )

        for name, value in iterable:
            if name.isupper():
                setattr(self, name, value)

    def to_dict(self):
        """Create a dict represenation of the settings
        Only uppercase attributes are included

        Returns:
            dict: dict represenation
        """
        return {k: v for k, v in self.__dict__.items() if k.upper()}

    def __repr__(self) -> str:
        return "\n".join("{}={}".format(k, pformat(v, indent=2)) for k, v in self.__dict__.items() if k.isupper())


settings = Settings()
