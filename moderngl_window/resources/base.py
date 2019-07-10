"""
Base registry class
"""
import inspect
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Generator, Type, Tuple

from moderngl_window.conf import settings
from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.utils.module_loading import import_string


class ResourceDescription:
    """ Description of any resource.
    Resource descriptions are required to load a resource.
    """
    default_kind = None  # The default kind of loader
    resource_type = None  # What resource type is described

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    @property
    def path(self):
        """str: The path to a resource when a single file is specified"""
        return self._kwargs.get('path')

    @property
    def kind(self):
        """str: default resource kind"""
        return self._kwargs.get('kind') or self.default_kind

    @kind.setter
    def kind(self, value):
        self._kwargs['kind'] = value

    @property
    def loader_cls(self) -> Type:
        """Type: The loader class for this resource"""
        return self._kwargs.get('loader_cls')

    @loader_cls.setter
    def loader_cls(self, value: Type):
        self._kwargs['loader_cls'] = value

    @property
    def resolved_path(self) -> Path:
        """pathlib.Path: The resolved path by a finder"""
        return self.kwargs.get('resolved_path')

    @resolved_path.setter
    def resolved_path(self, value: Path):
        self._kwargs['resolved_path'] = value

    @property
    def kwargs(self) -> Dict[str, str]:
        """dict: All keywords arguments passed to the resource"""
        return self._kwargs

    def __str__(self):
        return str(self._kwargs)

    def __repr__(self):
        return str(self)


class BaseRegistry:
    """Base class for all resource pools"""
    settings_attr = None

    def __init__(self):
        self._resources = []

    @property
    def count(self) -> int:
        """int: The number of ResourceDescroptions added.
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
        Loads a resource using the configured finders and loaders

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
        pool using `add()`.

        Returns:
            Generator of (meta, resoure) tuples
        """
        for meta in self._resources:
            resource = self.load(meta)
            yield meta, resource

        self._resources = []

    def resolve_loader(self, meta: ResourceDescription, raise_on_error=True):
        """
        Attempts to assign a loader class to a ResourceDecription.

        Args:
            meta (ResourceDescription): The resource description instance
        """
        self._check_meta(meta)

        # Get loader using kind if specified
        if meta.kind:
            for loader_cls in self.loaders:
                if loader_cls.kind == meta.kind:
                    meta.loader_cls = loader_cls
                    return

        # Get loader based on file extension
        for loader_cls in self.loaders:
            if loader_cls.supports_file(meta):
                meta.loader_cls = loader_cls
                return

        if raise_on_error:
            raise ImproperlyConfigured(
                "Resource has invalid loader '{}': {}\nAvailiable loaders: {}".format(
                    meta.loader, meta, [loader.kind for loader in self.loaders]))

    def _check_meta(self, meta: Any):
        """Check is the instance is a resource description
        Raises:
            ImproperlyConfigured if not a ResourceDescription instance
        """
        if inspect.isclass(type(meta)):
            if issubclass(meta.__class__, ResourceDescription):
                return

        raise ImproperlyConfigured("Resource loader got type {}, not a resource description".format(type(meta)))
