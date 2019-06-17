"""Scene Regisry"""
from moderngl_window.conf import settings
from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.resources.meta import SceneDescription
from moderngl_window.resources.base import BaseRegistry
from moderngl_window.utils.module_loading import import_string


class Scenes(BaseRegistry):
    """
    A registry for scense requested by effects.
    Once all effects are initialized, we ask this class to load the scenes.
    """
    def __init__(self):
        super().__init__()
        self._loaders = [
            import_string(loader) for loader in settings.SCENE_LOADERS
        ]

    def resolve_loader(self, meta: SceneDescription):
        """
        Resolve scene loader based on file extension
        """
        for loader_cls in self._loaders:
            if loader_cls.supports_file(meta):
                meta.loader_cls = loader_cls
                break
        else:
            raise ImproperlyConfigured(
                "Scene {} has no loader class registered. Check settings.SCENE_LOADERS".format(meta.path))


scenes = Scenes()
