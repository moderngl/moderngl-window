from moderngl_window.finders import base
from moderngl_window.conf import settings


class FilesystemFinder(base.BaseFilesystemFinder):
    """Find textures in ``settings.TEXTURE_DIRS``"""

    settings_attr = "TEXTURE_DIRS"


def get_finders():
    for finder in settings.TEXTURE_FINDERS:
        yield base.get_finder(finder)
