from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Union

from moderngl_window.conf import settings


@contextmanager
def texture_dirs(paths: list[Union[Path, str]]) -> Generator[None, None, None]:
    """Context manager temporarily replacing texture paths
    Args:
        paths (list[Union[Path, str]]): list of paths
    """
    original_dirs = settings.DATA_DIRS
    settings.TEXTURE_DIRS = paths
    yield None
    settings.TEXTURE_DIRS = original_dirs
