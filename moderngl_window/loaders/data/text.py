import logging

from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.loaders.base import BaseLoader

logger = logging.getLogger(__name__)


class Loader(BaseLoader):
    kind = "text"
    file_extensions = [
        [".txt"],
    ]

    def load(self) -> str:
        """Load a file in text mode.

        Returns:
            str: The string contents of the file
        """
        assert self.meta.path is not None, "the path is empty for this loader"
        self.meta.resolved_path = self.find_data(self.meta.path)

        if not self.meta.resolved_path:
            raise ImproperlyConfigured("Data file '{}' not found".format(self.meta.path))

        logger.info("Loading: %s", self.meta.path)

        with open(str(self.meta.resolved_path), "r") as fd:
            return fd.read()
