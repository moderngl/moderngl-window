from pathlib import Path
from typing import Any

import moderngl_window
from moderngl_window.finders import data, program, scenes, textures


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

        return self._find_last_of(Path(path), data.get_finders())

    def find_program(self, path):
        if not path:
            return None

        return self._find_last_of(Path(path), program.get_finders())

    def find_texture(self, path):
        if not path:
            return None

        return self._find_last_of(Path(path), textures.get_finders())

    def find_scene(self, path):
        if not path:
            return None

        return self._find_last_of(Path(path), scenes.get_finders())

    def _find_last_of(self, path, finders):
        """Find the last occurance of the file in finders"""
        found_path = None
        for finder in finders:
            result = finder.find(path)
            if result:
                found_path = result

        return found_path

    @property
    def ctx(self):
        """ModernGL context"""
        return moderngl_window.ctx()
