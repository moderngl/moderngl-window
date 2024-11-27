from moderngl_window.finders import base
from moderngl_window.conf import settings

from collections.abc import Iterator


class FilesystemFinder(base.BaseFilesystemFinder):
    """Find data in ``settings.DATA_DIRS``"""

    settings_attr = "DATA_DIRS"


def get_finders() -> Iterator[base.BaseFilesystemFinder]:
    for finder in settings.DATA_FINDERS:
        yield base.get_finder(finder)
