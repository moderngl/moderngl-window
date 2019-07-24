import logging
from pathlib import Path
from typing import Any

import moderngl
import moderngl_window as mglw
from moderngl_window.finders import data, program, scene, texture

logger = logging.getLogger(__name__)


class BaseLoader:
    """
    Base loader class for all resources.
    """
    #: The kind of resource this loaded supports.
    #: This can be used when file extensions is not enough
    #: to decide what loader should be selected.
    kind = None  # Type: str
    file_extensions = []

    def __init__(self, meta):
        """
        Args:
            meta (ResourceDescription): The resource to load
        """
        self.meta = meta
        if self.kind is None:
            raise ValueError("Loader {} doesn't have a kind".format(self.__class__))

    @classmethod
    def supports_file(cls, meta):
        """Check if the loader has a supported file extension"""
        path = Path(meta.path)

        for ext in cls.file_extensions:
            if path.suffixes[:len(ext)] == ext:
                return True

        return False

    def load(self) -> Any:
        """Load a resource

        Returns:
            The loaded resource
        """
        raise NotImplementedError()

    def find_data(self, path):
        """Find resource using data finders.
        Args:
            path: Path to resource
        """
        return self._find(Path(path), data.get_finders())

    def find_program(self, path):
        """Find resource using program finders.
        Args:
            path: Path to resource
        """
        return self._find(Path(path), program.get_finders())

    def find_texture(self, path):
        """Find resource using texture finders.
        Args:
            path: Path to resource
        """
        return self._find(Path(path), texture.get_finders())

    def find_scene(self, path):
        """Find resource using scene finders.
        Args:
            path: Path to resource
        """
        return self._find(Path(path), scene.get_finders())

    def _find(self, path: Path, finders: list):
        """Find the first occurance of this path in all finders.

        Args:
            path (Path): The path to find
        """
        if not path:
            return None

        for finder in finders:
            result = finder.find(path)
            if result:
                return result

        logger.debug("No finder was able to locate: %s", path)
        return None

    @property
    def ctx(self) -> moderngl.Context:
        """moderngl.Context: ModernGL context.
        Resources like textures and shader progams do need a context.
        """
        return mglw.ctx()
