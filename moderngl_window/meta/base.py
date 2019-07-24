from pathlib import Path
from typing import Dict, Type


class ResourceDescription:
    """ Description of any resource.
    Resource descriptions are required to load a resource.
    """
    default_kind = None  # The default kind of loader
    resource_type = None  # What resource type is described

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    @property
    def path(self) -> str:
        """str: The path to a resource when a single file is specified"""
        return self._kwargs.get('path')

    @property
    def label(self) -> str:
        """str: optional name for the resource"""
        return self._kwargs.get('label')

    @property
    def kind(self) -> str:
        """str: default resource kind"""
        return self._kwargs.get('kind') or self.default_kind

    @kind.setter
    def kind(self, value) -> str:
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
        return self._kwargs.get('resolved_path')

    @resolved_path.setter
    def resolved_path(self, value: Path):
        self._kwargs['resolved_path'] = value

    @property
    def attrs(self) -> Dict[str, str]:
        """dict: All keywords arguments passed to the resource"""
        return self._kwargs

    def __str__(self):
        return str(self._kwargs)

    def __repr__(self):
        return str(self)
