import json
import logging

from moderngl_window.loaders.base import BaseLoader
from moderngl_window.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)


class Loader(BaseLoader):
    kind = "json"
    file_extensions = [
        [".json"],
    ]

    def load(self) -> dict:
        """Load a file as json

        Returns:
            dict: The json contents
        """
        self.meta.resolved_path = self.find_data(self.meta.path)

        if not self.meta.resolved_path:
            raise ImproperlyConfigured(
                "Data file '{}' not found".format(self.meta.path)
            )

        logger.info("Loading: %s", self.meta.path)

        with open(str(self.meta.resolved_path), "r") as fd:
            return json.loads(fd.read())
