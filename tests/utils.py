import random
import string
from contextlib import contextmanager

from moderngl_window import conf


@contextmanager
def settings_context(values: dict):
    """Override conf.settings

    Args:
        values (dict): Dictionary containing settings values
    """
    old_settings = conf.settings.to_dict()
    conf.settings.apply_from_dict(values)
    yield None
    conf.settings.apply_from_dict(old_settings)


def rnd_string(length=16):
    chars = string.ascii_letters + string.digits
    return "".join(c for c in random.choices(chars, k=length))
