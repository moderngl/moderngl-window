import logging

from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.loaders.base import BaseLoader

logger = logging.getLogger(__name__)


class Loader(BaseLoader):
    kind = "binary"

    def load(self) -> bytes:
        """Load a file in binary mode

        Returns:
            bytes: The bytes contents of the file
        """
        self.meta.resolved_path = self.find_data(self.meta.path)

        if not self.meta.resolved_path:
            raise ImproperlyConfigured("Data file '{}' not found".format(self.meta.path))

        logger.info("Loading: %s", self.meta.path)

        with open(str(self.meta.resolved_path), "rb") as fd:
            return fd.read()
