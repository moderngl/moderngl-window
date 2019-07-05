"""
Base finders
"""
import functools
from collections import namedtuple
from pathlib import Path

from moderngl_window.conf import settings
from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.utils.module_loading import import_string

FinderEntry = namedtuple('FinderEntry', ['path', 'abspath', 'exists'])


class BaseFileSystemFinder:
    """Base class for searching directories"""
    settings_attr = None

    def __init__(self):
        if not hasattr(settings, self.settings_attr):
            raise ImproperlyConfigured(
                "Settings doesn't define {}. "
                "This is required when using a FileSystemFinder.".format(self.settings_attr)
            )
        self.paths = getattr(settings, self.settings_attr)

    def find(self, path: Path) -> Path:
        """
        Find a file in the path. The file may exist in multiple
        paths. The last found file will be returned.

        Args:
            path (Path): The path to find

        Returns:
            The absolute path to the file or None if not found
        """
        # Update paths from settings to make them editable runtime
        # This is only possible for FileSystemFinders
        if getattr(self, 'settings_attr', None):
            self.paths = getattr(settings, self.settings_attr)

        for entry in self.paths:
            abspath = entry / path
            if abspath.exists():
                return abspath

        return None


@functools.lru_cache(maxsize=None)
def get_finder(import_path: str):
    """
    Get a finder class from an import path.
    This function uses an lru cache.

    Args:
        import_path: string representing an import path

    Return:
        An instance of the finder
 
    Raises:
        ImproperlyConfigured is the finder is not found
    """
    Finder = import_string(import_path)
    if not issubclass(Finder, BaseFileSystemFinder):
        raise ImproperlyConfigured('Finder {} is not a subclass of .finders.FileSystemFinder'.format(import_path))

    return Finder()
