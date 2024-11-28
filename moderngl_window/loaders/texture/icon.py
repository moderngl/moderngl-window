from pathlib import Path

from moderngl_window.finders import texture
from moderngl_window.loaders.base import BaseLoader
from moderngl_window.meta.base import ResourceDescription
from moderngl_window.meta.texture import TextureDescription


class IconLoader(BaseLoader):
    kind = "icon"
    meta: TextureDescription

    def __init__(self, meta: ResourceDescription) -> None:
        super().__init__(meta)

    def find_icon(self) -> Path:
        """Find resource using texture finders.

        This is mainly a shortcut method to simplify the task.

        Args:
            path: Path to resource
        """
        abs_path = self._find(self.meta.path, texture.get_finders())
        if abs_path is None:
            raise ValueError("Could not find the icon specified. {}".format(self.meta.path))
        return abs_path
