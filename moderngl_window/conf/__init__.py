"""
Bag of settings values
"""

# pylint: disable = invalid-name
import importlib
import os
import pathlib
from collections.abc import Generator, Iterable
from pprint import pformat
from types import ModuleType as Module
from typing import Any, Optional, Union

from moderngl_window.conf import default
from moderngl_window.exceptions import ImproperlyConfigured

SETTINGS_ENV_VAR = "MODERNGL_WINDOW_SETTINGS_MODULE"


class Settings:
    """
    Bag of settings values. New attributes can be freely added runtime.
    Various apply* methods are supplied so the user have full control over how
    settings values are initialized. This is especially useful for more custom usage.
    And instance of the `Settings` class is created when the `conf` module is imported.

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

        # Pretty printed string representation for easy inspection
        print(settings)
    """

    WINDOW: dict[str, Any] = dict()
    """
    Window/screen properties. Most importantly the ``class`` attribute
    decides what class should be used to handle the window.

    .. code:: python

        # Default values
        WINDOW = {
            "gl_version": (3, 3),
            "class": "moderngl_window.context.pyglet.Window",
            "size": (1280, 720),
            "aspect_ratio": 16 / 9,
            "fullscreen": False,
            "resizable": True,
            "title": "ModernGL Window",
            "vsync": True,
            "cursor": True,
            "samples": 0,
        }

    Other Properties:

    - ``gl_version``: The minimum required major/minor OpenGL version
    - ``size``: The window size to open.
    - ``aspect_ratio`` is the enforced aspect ratio of the viewport.
    - ``fullscreen``: True if you want to create a context in fullscreen mode
    - ``resizable``: If the window should be resizable. This only applies in
      windowed mode.
    - ``vsync``: Only render one frame per screen refresh
    - ``title``: The visible title on the window in windowed mode
    - ``cursor``: Should the mouse cursor be visible on the screen? Disabling
      this is also useful in windowed mode when controlling the camera on some
      platforms as moving the mouse outside the window can cause issues.
    - ``Samples``: Number if samples used in multisampling. Values above 1
      enables multisampling.

    The created window frame buffer will by default use:

    - RGBA8 (32 bit per pixel)
    - 24 bit depth buffer
    - Double buffering
    - color and depth buffer is cleared for every frame

    """
    SCREENSHOT_PATH: Optional[str] = None
    """
    Absolute path to the directory screenshots will be saved by the screenshot module.
    Screenshots will end up in the project root of not defined.
    If a path is configured, the directory will be auto-created.
    """
    # Finders
    PROGRAM_FINDERS: list[str] = []
    """
    Finder classes for locating programs/shaders.

    .. code:: python

        # Default values
        PROGRAM_FINDERS = [
            "moderngl_window.finders.program.FileSystemFinder",
        ]
    """
    TEXTURE_FINDERS: list[str] = []
    """
    Finder classes for locating textures.

    .. code:: python

        # Default values
        TEXTURE_FINDERS = [
            "moderngl_window.finders.texture.FileSystemFinder",
        ]
    """
    SCENE_FINDERS: list[str] = []
    """
    Finder classes for locating scenes.

    .. code:: python

        # Default values
        SCENE_FINDERS = [
            "moderngl_window.finders.scene.FileSystemFinder",
        ]

    """
    DATA_FINDERS: list[str] = []
    """
    Finder classes for locating data files.

    .. code:: python

        # Default values
        DATA_FINDERS = [
            "moderngl_window.finders.data.FileSystemFinder",
        ]
    """
    # Finder dirs
    PROGRAM_DIRS: list[Union[str, pathlib.Path]] = []
    """
    Lists of `str` or `pathlib.Path` used by ``FileSystemFinder``
    to looks for programs/shaders.
    """
    TEXTURE_DIRS: list[Union[str, pathlib.Path]] = []
    """
    Lists of `str` or `pathlib.Path` used by ``FileSystemFinder``
    to looks for textures.
    """
    SCENE_DIRS: list[Union[str, pathlib.Path]] = []
    """
    Lists of `str` or `pathlib.Path` used by ``FileSystemFinder``
    to looks for scenes (obj, gltf, stl etc).
    """
    DATA_DIRS: list[Union[str, pathlib.Path]] = []
    """
    Lists of `str` or `pathlib.Path` used by ``FileSystemFinder``
    to looks for data files.
    """

    # Loaders
    PROGRAM_LOADERS: list[str] = []
    """
    Classes responsible for loading programs/shaders.

    .. code:: python

        # Default values
        PROGRAM_LOADERS = [
            'moderngl_window.loaders.program.single.Loader',
            'moderngl_window.loaders.program.separate.Loader',
        ]
    """
    TEXTURE_LOADERS: list[str] = []
    """
    Classes responsible for loading textures.

    .. code:: python

        # Default values
        TEXTURE_LOADERS = [
            'moderngl_window.loaders.texture.t2d.Loader',
            'moderngl_window.loaders.texture.array.Loader',
        ]
    """
    SCENE_LOADERS: list[str] = []
    """
    Classes responsible for loading scenes.

    .. code:: python

        # Default values
        SCENE_LOADERS = [
            "moderngl_window.loaders.scene.gltf.GLTF2",
            "moderngl_window.loaders.scene.wavefront.ObjLoader",
            "moderngl_window.loaders.scene.stl_loader.STLLoader",
        ]

    """
    DATA_LOADERS: list[str] = []
    """
    Classes responsible for loading data files.

    .. code:: python

        # Default values
        DATA_LOADERS = [
            'moderngl_window.loaders.data.binary.Loader',
            'moderngl_window.loaders.data.text.Loader',
            'moderngl_window.loaders.data.json.Loader',
        ]
    """

    def __init__(self) -> None:
        """Initialize settings with default values"""
        self.apply_default_settings()

    def apply_default_settings(self) -> None:
        """
        Apply keys and values from the default settings module
        located in this package. This is to ensure we always
        have the minimal settings for the system to run.

        If replacing or customizing the settings class
        you must always apply default settings to ensure
        compatibility when new settings are added.
        """
        self.apply_from_module(default)

    def apply_settings_from_env(self) -> None:
        """
        Apply settings from ``MODERNGL_WINDOW_SETTINGS_MODULE`` environment variable.
        If the environment variable is undefined no action will be taken.
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
        except ImportError as ex:
            raise ImproperlyConfigured(
                "Settings module '{}' not found. From importlib: {}".format(
                    settings_module_name,
                    ex,
                )
            )

        self.apply_from_module(module)

    def apply_from_dict(self, data: dict[str, Any]) -> None:
        """
        Apply settings values from a dictionary

        Example::

            >> from moderngl_window.conf import settings
            >> settings.apply_dict({'SOME_VALUE': 1})
            >> settings.SOME_VALUE
            1
        """
        self.apply_from_iterable(data.items())

    def apply_from_module(self, module: Module) -> None:
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

    def apply_from_cls(self, cls: Any) -> None:
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

    def apply_from_iterable(self, iterable: Iterable[tuple[str, Any]]) -> None:
        """
        Apply (key, value) pairs from an iterable or generator
        """
        if not isinstance(iterable, Iterable) and not isinstance(self, Generator):
            raise ValueError(
                "Input value is not a generator or iterable, but of type: {}".format(type(iterable))
            )

        for name, value in iterable:
            if name.isupper():
                setattr(self, name, value)

    def to_dict(self) -> dict[str, Any]:
        """Create a dict representation of the settings
        Only uppercase attributes are included

        Returns:
            dict: dict representation
        """
        return {k: v for k, v in self.__dict__.items() if k.upper()}

    def __repr__(self) -> str:
        return "\n".join(
            "{}={}".format(k, pformat(v, indent=2)) for k, v in self.__dict__.items() if k.isupper()
        )


settings = Settings()
