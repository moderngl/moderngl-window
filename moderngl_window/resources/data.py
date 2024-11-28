"""
Registry general data files
"""

from typing import Any

from moderngl_window.meta import DataDescription, ResourceDescription
from moderngl_window.resources.base import BaseRegistry


class DataFiles(BaseRegistry):
    """Registry for requested data files"""

    settings_attr = "DATA_LOADERS"
    meta: DataDescription

    def load(self, meta: ResourceDescription) -> Any:
        """Load data file with the configured loaders.

        Args:
            meta (:py:class:`~moderngl_window.meta.data.DataDescription`): the resource description
        Returns:
            Any: The loaded resource
        """
        return super().load(meta)


data = DataFiles()
