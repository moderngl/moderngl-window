import logging
from pathlib import Path
from typing import Any

import moderngl_window as mglw
from moderngl_window.finders import data, program, scene, texture

logger = logging.getLogger(__name__)


class BaseLoader:
    """
    Base loader class for all resources
    """

    def __init__(self, meta):
        """
        :param meta: ResourceDescription instance
        """
        self.meta = meta

    def load(self) -> Any:
        """
        Load a resource

        :returns: The newly loaded resource
        """
        raise NotImplementedError()

    def find_data(self, path):
        if not path:
            return None

        return self._find(Path(path), data.get_finders())

    def find_program(self, path):
        if not path:
            return None

        return self._find(Path(path), program.get_finders())

    def find_texture(self, path):
        if not path:
            return None

        return self._find(Path(path), texture.get_finders())

    def find_scene(self, path):
        if not path:
            return None

        return self._find(Path(path), scene.get_finders())

    def _find(self, path, finders):
        """Find the first occurance of the file"""
        for finder in finders:
            result = finder.find(path)
            if result:
                return result

        logger.debug("No finder was able to locate: %s", path)
        return None

    @property
    def ctx(self):
        """ModernGL context"""
        return mglw.ctx()
