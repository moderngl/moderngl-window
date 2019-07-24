from pathlib import Path
from typing import List, Union

from contextlib import contextmanager
from moderngl_window.conf import settings


@contextmanager
def texture_dirs(paths: List[Union[Path, str]]):
    """Context manager temporarily replacing texture paths
    Args:
        paths (List[Union[Path, str]]): list of paths
    """
    original_dirs = settings.DATA_DIRS
    settings.TEXTURE_DIRS = paths
    yield None
    settings.TEXTURE_DIRS = original_dirs
