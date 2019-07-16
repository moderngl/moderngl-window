"""
Scene Regisry
"""
from moderngl_window.resources.base import BaseRegistry
from moderngl_window.scene import Scene
from moderngl_window.meta import SceneDescription


class Scenes(BaseRegistry):
    """
    A registry for scense requested by effects.
    Once all effects are initialized, we ask this class to load the scenes.
    """
    settings_attr = 'SCENE_LOADERS'

    def load(self, meta: SceneDescription) -> Scene:
        """Load a scene with the configurred loaders"""
        return super().load(meta)


scenes = Scenes()
