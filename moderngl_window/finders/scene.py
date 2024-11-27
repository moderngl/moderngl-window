from moderngl_window.finders import base
from moderngl_window.conf import settings

from collections.abc import Iterator


class FilesystemFinder(base.BaseFilesystemFinder):
    """Find scenes in ``settings.SCENE_DIRS``"""

    settings_attr = "SCENE_DIRS"


def get_finders() -> Iterator[base.BaseFilesystemFinder]:
    for finder in settings.SCENE_FINDERS:
        yield base.get_finder(finder)
