"""
Shader Registry
"""
from moderngl_window.resources.base import BaseRegistry


class Textures(BaseRegistry):
    """
    A registry for textures requested by effects.
    Once all effects are initialized, we ask this class to load the textures.
    """
    settings_attr = 'TEXTURE_DIRS'


textures = Textures()
