import logging
from pathlib import Path
from typing import Any

import moderngl
import moderngl_window as mglw
from moderngl_window.finders import data, program, scene, texture

logger = logging.getLogger(__name__)


class BaseLoader:
    """Base loader class for all resources"""
    kind = "unknown"
    """
    The kind of resource this loaded supports.
    This can be used when file extensions is not enough
    to decide what loader should be selected.
    """
    file_extensions = []
    """
    A list defining the file extensions accepted by this loader.

    Example::

        # Loader will match .xyz and .xyz.gz files.
        file_extensions = [
            ['.xyz'],
            ['.xyz', '.gz'],
        ]
    """

    def __init__(self, meta):
        """Initialize loader.

        Loaders take a ResourceDescription instance
        containing all the parameters needed to load and initialize
        this data.

        Args:
            meta (ResourceDescription): The resource to load
        """
        self.meta = meta
        if self.kind is None:
            raise ValueError("Loader {} doesn't have a kind".format(self.__class__))

    @classmethod
    def supports_file(cls, meta):
        """Check if the loader has a supported file extension.

        What extensions are supported can be defined in the
        :py:attr:`file_extensions` class attribute.
        """
        path = Path(meta.path)

        for ext in cls.file_extensions:
            if path.suffixes[: len(ext)] == ext:
                return True

        return False

    def load(self) -> Any:
        """Loads a resource.

        When creating a loader this is the only
        method that needs to be implemented.

        Returns:
            The loaded resource
        """
        raise NotImplementedError()

    def find_data(self, path):
        """Find resource using data finders.

        This is mainly a shortcut method to simplify the task.

        Args:
            path: Path to resource
        """
        return self._find(Path(path), data.get_finders())

    def find_program(self, path):
        """Find resource using program finders.

        This is mainly a shortcut method to simplify the task.

        Args:
            path: Path to resource
        """
        return self._find(Path(path), program.get_finders())

    def find_texture(self, path):
        """Find resource using texture finders.

        This is mainly a shortcut method to simplify the task.

        Args:
            path: Path to resource
        """
        return self._find(Path(path), texture.get_finders())

    def find_scene(self, path):
        """Find resource using scene finders.

        This is mainly a shortcut method to simplify the task.

        Args:
            path: Path to resource
        """
        return self._find(Path(path), scene.get_finders())

    def _find(self, path: Path, finders: list):
        """Find the first occurrance of this path in all finders.
        If the incoming path is an absolute path we assume this
        path exist and return it.

        Args:
            path (Path): The path to find
        """
        if not path:
            return None

        if path.is_absolute():
            return path

        for finder in finders:
            result = finder.find(path)
            if result:
                return result

        logger.debug("No finder was able to locate: %s", path)
        return None

    @property
    def ctx(self) -> moderngl.Context:
        """moderngl.Context: ModernGL context"""
        return mglw.ctx()
