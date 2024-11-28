"""
Scene Registry
"""

from moderngl_window.meta import ResourceDescription, SceneDescription
from moderngl_window.resources.base import BaseRegistry
from moderngl_window.scene import Scene


class Scenes(BaseRegistry):
    """Handles scene loading"""

    settings_attr = "SCENE_LOADERS"
    meta: SceneDescription

    def load(self, meta: ResourceDescription) -> Scene:
        """Load a scene with the configured loaders.

        Args:
            meta (:py:class:`~moderngl_window.meta.scene.SceneDescription`):
            The resource description
        Returns:
            :py:class:`~moderngl_window.scene.Scene`: The loaded scene
        """
        scene = super().load(meta)
        assert isinstance(
            scene, Scene
        ), f"{meta} did not load a moderngl_window.scene.Scene object, please correct it."
        return scene


scenes = Scenes()
