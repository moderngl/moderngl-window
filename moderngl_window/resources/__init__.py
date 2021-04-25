from contextlib import contextmanager
from pathlib import Path
from typing import Union

from moderngl_window.conf import settings
from moderngl_window.exceptions import ImproperlyConfigured

from moderngl_window.resources.programs import programs  # noqa
from moderngl_window.resources.textures import textures  # noqa

# from moderngl_window.resources.tracks import tracks  # noqa
from moderngl_window.resources.scenes import scenes  # noqa
from moderngl_window.resources.data import data  # noqa


def register_dir(path: Union[Path, str]) -> None:
    """Adds a resource directory for all resource types

    Args:
        path (Union[Path, str]): Directory path
    """
    register_data_dir(path)
    register_program_dir(path)
    register_scene_dir(path)
    register_texture_dir(path)


def register_program_dir(path: Union[Path, str]) -> None:
    """Adds a resource directory specifically for programs

    Args:
        path (Union[Path, str]): Directory path
    """
    _append_unique_path(path, settings.PROGRAM_DIRS)


def register_texture_dir(path: Union[Path, str]) -> None:
    """Adds a resource directory specifically for textures

    Args:
        path (Union[Path, str]): Directory path
    """
    _append_unique_path(path, settings.TEXTURE_DIRS)


def register_scene_dir(path: Union[Path, str]) -> None:
    """Adds a resource directory specifically for scenes

    Args:
        path (Union[Path, str]): Directory path
    """
    _append_unique_path(path, settings.SCENE_DIRS)


def register_data_dir(path: Union[Path, str]) -> None:
    """Adds a resource directory specifically for data files

    Args:
        path (Union[Path, str]): Directory path
    """
    _append_unique_path(path, settings.DATA_DIRS)


def _append_unique_path(path: Union[Path, str], dest: list):
    path = Path(path)
    if not path.is_absolute():
        raise ImproperlyConfigured("Search path must be absolute: {}".format(path))

    if not path.is_dir():
        raise ImproperlyConfigured("Search path is not a directory: {}".format(path))

    if not path.exists():
        raise ImproperlyConfigured("Search path do not exist: {}".format(path))

    for resource_path in dest:
        if Path(resource_path).samefile(path):
            break
    else:
        dest.append(Path(path).absolute())


@contextmanager
def temporary_dirs(dirs: Union[Path, str] = []):
    """Temporarily changes all resource directories

    Example::

        with temporary_dirs([path1, path2, path3]):
            # Load some resource here

    Args:
        dirs (Union[Path,str]) list of paths to use
    """
    data_dirs = settings.DATA_DIRS
    program_dirs = settings.PROGRAM_DIRS
    scene_dirs = settings.SCENE_DIRS
    textures_dirs = settings.TEXTURE_DIRS

    settings.DATA_DIRS = dirs
    settings.PROGRAM_DIRS = dirs
    settings.SCENE_DIRS = dirs
    settings.TEXTURE_DIRS = dirs

    try:
        yield dirs
    finally:
        settings.DATA_DIRS = data_dirs
        settings.PROGRAM_DIRS = program_dirs
        settings.SCENE_DIRS = scene_dirs
        settings.TEXTURE_DIRS = textures_dirs
