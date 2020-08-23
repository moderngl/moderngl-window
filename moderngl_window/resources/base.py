"""
Base registry class
"""
import inspect
from functools import lru_cache
from typing import Any, Generator, Tuple

from moderngl_window.conf import settings
from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.utils.module_loading import import_string
from moderngl_window.meta.base import ResourceDescription


class BaseRegistry:
    """Base class for all resource pools"""

    settings_attr = None
    """str: The name of the attribute in :py:class:`~moderngl_window.conf.Settings`
    containting a list of loader classes.
    """

    def __init__(self):
        """Initialize internal attributes"""
        self._resources = []

    @property
    def count(self) -> int:
        """int: The number of resource descriptions added.
        This is only relevant when using `add` and `load_pool`.
        """
        return len(self._resources)

    @property
    def loaders(self):
        """Generator: Loader classes for this resource type"""
        for loader in getattr(settings, self.settings_attr):
            yield self._loader_cls(loader)

    @lru_cache(maxsize=None)
    def _loader_cls(self, python_path: str):
        return import_string(python_path)

    def load(self, meta: ResourceDescription) -> Any:
        """
        Loads a resource using the configured finders and loaders.

        Args:
            meta (ResourceDescription): The resource description
        """
        self._check_meta(meta)
        self.resolve_loader(meta)
        return meta.loader_cls(meta).load()

    def add(self, meta: ResourceDescription) -> None:
        """
        Adds a resource description without loading it.
        The resource is loaded and returned when ``load_pool()`` is called.

        Args:
            meta (ResourceDescription): The resource description
        """
        self._check_meta(meta)
        self.resolve_loader(meta)
        self._resources.append(meta)

    def load_pool(self) -> Generator[Tuple[ResourceDescription, Any], None, None]:
        """
        Loads all the data files using the configured finders.

        This is only relevant when resource have been added to this
        pool using ``add()``.

        Returns:
            Generator of (meta, resource) tuples
        """
        for meta in self._resources:
            resource = self.load(meta)
            yield meta, resource

        self._resources = []

    def resolve_loader(self, meta: ResourceDescription) -> None:
        """
        Attempts to assign a loader class to a ResourceDescription.

        Args:
            meta (:py:class:`~moderngl_window.meta.base.ResourceDescription`): The resource description instance
        """
        # Get loader using kind if specified
        if meta.kind:
            for loader_cls in self.loaders:
                if loader_cls.kind == meta.kind:
                    meta.loader_cls = loader_cls
                    return

            raise ImproperlyConfigured(
                "Resource has invalid loader kind '{}': {}\nAvailable loaders: {}".format(
                    meta.kind, meta, [loader.kind for loader in self.loaders]
                )
            )

        # Get loader based on file extension
        for loader_cls in self.loaders:
            if loader_cls.supports_file(meta):
                meta.loader_cls = loader_cls
                return

        raise ImproperlyConfigured("Could not find a loader for: {}".format(meta))

    def _check_meta(self, meta: Any):
        """Check is the instance is a resource description
        Raises:
            ImproperlyConfigured if not a ResourceDescription instance
        """
        if inspect.isclass(type(meta)):
            if issubclass(meta.__class__, ResourceDescription):
                return

        raise ImproperlyConfigured(
            "Resource loader got type {}, not a resource description".format(type(meta))
        )
