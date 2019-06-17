"""
Registry general data files
"""
from moderngl_window.conf import settings
from moderngl_window.resources.base import BaseRegistry
from moderngl_window.utils.module_loading import import_string


class DataFiles(BaseRegistry):
    """Registry for requested data files"""
    def __init__(self):
        super().__init__()
        self._loaders = [
            import_string(loader) for loader in settings.DATA_LOADERS
        ]


data = DataFiles()
