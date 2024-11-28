from collections.abc import Iterator

from moderngl_window.conf import settings
from moderngl_window.finders import base


class FilesystemFinder(base.BaseFilesystemFinder):
    """Find shaders in ``settings.PROGRAM_DIRS``"""

    settings_attr = "PROGRAM_DIRS"


def get_finders() -> Iterator[base.BaseFilesystemFinder]:
    for finder in settings.PROGRAM_FINDERS:
        yield base.get_finder(finder)
