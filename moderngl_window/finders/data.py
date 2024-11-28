from collections.abc import Iterable

from moderngl_window.conf import settings
from moderngl_window.finders import base


class FilesystemFinder(base.BaseFilesystemFinder):
    """Find data in ``settings.DATA_DIRS``"""

    settings_attr = "DATA_DIRS"


def get_finders() -> Iterable[base.BaseFilesystemFinder]:
    for finder in settings.DATA_FINDERS:
        yield base.get_finder(finder)
