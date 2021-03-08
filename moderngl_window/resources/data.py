"""
Registry general data files
"""
from typing import Any
from moderngl_window.resources.base import BaseRegistry
from moderngl_window.meta import DataDescription


class DataFiles(BaseRegistry):
    """Registry for requested data files"""

    settings_attr = "DATA_LOADERS"

    def load(self, meta: DataDescription) -> Any:
        """Load data file with the configured loaders.

        Args:
            meta (:py:class:`~moderngl_window.meta.data.DataDescription`): the resource description
        Returns:
            Any: The loaded resource
        """
        return super().load(meta)


data = DataFiles()
