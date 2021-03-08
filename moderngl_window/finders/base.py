"""
Base finders
"""
import functools
import logging

from collections import namedtuple
from pathlib import Path

from moderngl_window.conf import settings
from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.utils.module_loading import import_string

FinderEntry = namedtuple("FinderEntry", ["path", "abspath", "exists"])

logger = logging.getLogger(__name__)


class BaseFilesystemFinder:
    """Base class for searching filesystem directories"""

    settings_attr = None
    """str: Name of the attribute in :py:class:`~moderngl_window.conf.Settings`
    containing a list of paths the finder should search in.
    """

    def __init__(self):
        """Initialize finder class by looking up the paths referenced in ``settings_attr``.
        """
        if not hasattr(settings, self.settings_attr):
            raise ImproperlyConfigured(
                "Settings doesn't define {}. "
                "This is required when using a FileSystemFinder.".format(
                    self.settings_attr
                )
            )
        self.paths = getattr(settings, self.settings_attr)

    def find(self, path: Path) -> Path:
        """Finds a file in the configured paths returning its absolute path.

        Args:
            path (pathlib.Path): The path to find
        Returns:
            The absolute path to the file or None if not found
        """
        # Update paths from settings to make them editable runtime
        if getattr(self, "settings_attr", None):
            self.paths = getattr(settings, self.settings_attr)

        if not isinstance(path, Path):
            raise ValueError(
                "FilesystemFinders only take Path instances, not {}".format(type(path))
            )

        logger.debug("find %s", path)

        # Ignore absolute paths so other finder types can pick them up.
        if path.is_absolute():
            logger.debug("Ignoring absolute path: %s", path)
            return None

        logger.debug("paths: %s", self.paths)

        for search_path in self.paths:
            search_path = Path(search_path)

            # Keep ensuring all search paths are absolute
            if not search_path.is_absolute():
                raise ImproperlyConfigured(
                    "Search search path '{}' is not an absolute path"
                )

            abspath = search_path / path
            logger.debug("abspath %s", abspath)

            if abspath.exists():
                logger.debug("found %s", abspath)
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
    if not issubclass(Finder, BaseFilesystemFinder):
        raise ImproperlyConfigured(
            "Finder {} is not a subclass of .finders.FileSystemFinder".format(
                import_path
            )
        )

    return Finder()
