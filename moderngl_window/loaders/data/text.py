from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.loaders.base import BaseLoader


class Loader(BaseLoader):
    kind = 'text'

    def load(self):
        """Load a file in text mode"""
        self.meta.resolved_path = self.find_data(self.meta.path)

        if not self.meta.resolved_path:
            raise ImproperlyConfigured("Data file '{}' not found".format(self.meta.path))

        print("Loading:", self.meta.path)

        with open(self.meta.resolved_path, 'r') as fd:
            return fd.read()
