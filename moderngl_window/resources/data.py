"""
Registry general data files
"""
from moderngl_window.resources.base import BaseRegistry


class DataFiles(BaseRegistry):
    """Registry for requested data files"""
    settings_attr = 'DATA_DIRS'


data = DataFiles()
