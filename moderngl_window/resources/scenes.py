"""
Scene Regisry
"""
from moderngl_window.resources.base import BaseRegistry


class Scenes(BaseRegistry):
    """
    A registry for scense requested by effects.
    Once all effects are initialized, we ask this class to load the scenes.
    """
    settings_attr = 'SCENE_LOADERS'


scenes = Scenes()
