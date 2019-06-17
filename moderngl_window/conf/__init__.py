"""
Bag of settings values
"""
import importlib
import types
import os

from collections.abc import Iterable
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
    """
    def __init__(self):
        """Initialize settings with default values"""
        # Set default entires. Mainly for code completion
        self.WINDOW = dict()
        # Finders
        self.PROGRAM_FINDERS = tuple()
        self.TEXTURE_FINDERS = tuple()
        self.SCENE_FINDERS = tuple()
        self.DATA_FINDERS = tuple()
        # Finder dirs
        self.PROGRAM_DIRS = tuple()
        self.TEXTURE_DIRS = tuple()
        self.SCENE_DIRS = tuple()
        self.DATA_DIRS = tuple()
        # Loaders
        self.PROGRAM_LOADERS = tuple()
        self.TEXTURE_LOADERS = tuple()
        self.SCENE_LOADERS = tuple()
        self.DATA_LOADERS = tuple()

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

        Example::

            import os
            os.environ['MODERNGL_WINDOW_SETTINGS_MODULE'] = 'python.path.to.module'
            settings.apply_settings_from_env()
        """
        name = os.environ.get(SETTINGS_ENV_VAR)
        if name:
            self.apply_from_module_name(name)

    def apply_from_module_name(self, settings_module_name: str) -> None:
        module = importlib.import_module(settings_module_name)
        if not module:
            raise ImproperlyConfigured(
                "Settings module '{}' not found. ".format(settings_module_name)
            )
        self.apply_from_module(module)

    def apply_from_dict(self, data: dict) -> None:
        """
        Apply settings values from a dictionary

        Example::

            >> settings.apply_dict({'SOME_VALUE': 1})
            >> settings.SOME_VALUE
            1
        """
        self.apply_from_iterable(data.items())

    def apply_from_module(self, module) -> None:
        """
        Apply settings values from a python module

        Example::

            my_settings.py module containing the following line:
            SOME_VALUE = 1

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

            >> class MySettings:
            >>    SOME_VALUE = 1
            >>
            >> settings.apply(MySettings)
            >> settings.SOME_VALUE
            1
        """
        for name, value in cls.__dict__.items():
            if name.isupper():
                setattr(self, name, value)

    def apply_from_iterable(self, iterable: Union[Iterable, types.GeneratorType]) -> None:
        if not isinstance(iterable, Iterable) and not isinstance(self, types.GeneratorType):
            raise ValueError(
                "Input value is not a generator or interable, but of type: {}".format(type(iterable))
            )

        for name, value in iterable:
            if name.isupper():
                setattr(self, name, value)

    def __repr__(self) -> str:
        return '<{cls} "{data}>"'.format(
            cls=self.__class__.__name__,
            data=None,
        )


settings = Settings()
