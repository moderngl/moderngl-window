from moderngl_window.finders import base
from moderngl_window.conf import settings


class FileSystemFinder(base.BaseFilesystemFinder):
    """Find shaders in ``PROGRAM_DIRS``"""
    settings_attr = 'PROGRAM_DIRS'


def get_finders():
    for finder in settings.PROGRAM_FINDERS:
        yield base.get_finder(finder)
