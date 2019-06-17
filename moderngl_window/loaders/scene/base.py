from pathlib import Path

from moderngl_window.loaders.base import BaseLoader
from moderngl_window.scene import Scene


class SceneLoader(BaseLoader):
    """Base class for object loaders"""
    # File extensions supported by this loader
    file_extensions = []

    def __init__(self, meta):
        super().__init__(meta)

    def load(self) -> Scene:
        """Load the scene"""
        raise NotImplementedError()

    @classmethod
    def supports_file(cls, meta):
        """Check if the loader has a supported file extension"""
        path = Path(meta.path)

        for ext in cls.file_extensions:
            if path.suffixes[:len(ext)] == ext:
                return True

        return False
