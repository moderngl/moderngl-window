from contextlib import contextmanager
from copy import deepcopy

from moderngl_window import conf


@contextmanager
def settings(values: dict):
    """Override conf.settings
    
    Args:
        values (dict): Dictionary containing settings values
    """
    class TempSettings:
        pass

    tmp_settings = TempSettings()

    # Copy settings values from original settings module
    for key, value in conf.settings.__dict__.items():
        if key.upper():
            setattr(tmp_settings, key, deepcopy(value))

    # Apply values from input dict
    for key, value in values.items():
        setattr(tmp_settings, key, deepcopy(value))

    # Replace settings instance
    conf.settings, original_settings = tmp_settings, conf.settings
    yield conf.settings

    # Restore order
    conf.settings = original_settings
