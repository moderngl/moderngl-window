"""Shader Registry"""
from moderngl_window.conf import settings
from moderngl_window.resources.base import BaseRegistry
from moderngl_window.utils.module_loading import import_string
from moderngl_window.resources.meta import ProgramDescription
from moderngl_window.exceptions import ImproperlyConfigured


class Programs(BaseRegistry):
    """
    A registry for shaders requested by effects.
    Once all effects are initialized, we ask this class to load the shaders.
    """
    def __init__(self):
        super().__init__()
        self._loaders = [
            import_string(loader) for loader in settings.PROGRAM_LOADERS
        ]

    def resolve_loader(self, meta: ProgramDescription):
        """
        Resolve program loader
        """
        if not meta.loader:
            meta.loader = 'single' if meta.path else 'separate'

        for loader_cls in self._loaders:
            if loader_cls.name == meta.loader:
                meta.loader_cls = loader_cls
                break
        else:
            raise ImproperlyConfigured(
                (
                    "Program {} has no loader class registered."
                    "Check PROGRAM_LOADERS or PROGRAM_DIRS"
                ).format(meta.path)
            )


programs = Programs()
