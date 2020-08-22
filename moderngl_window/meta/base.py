from pathlib import Path
from typing import Dict, Type


class ResourceDescription:
    """ Description of any resource.
    Resource descriptions are required to load a resource.
    This class can be extended to add more specific properties.
    """

    default_kind = None  # The default kind of loader
    """str: The default kind for this resource type"""
    resource_type = None  # What resource type is described
    """str: A unique identifier for the resource type"""

    def __init__(self, **kwargs):
        """Initialize a resource description

        Args:
            **kwargs: Attributes describing the resource to load
        """
        self._kwargs = kwargs

    @property
    def path(self) -> str:
        """str: The path to a resource when a single file is specified"""
        return self._kwargs.get("path")

    @property
    def label(self) -> str:
        """str: optional name for the resource

        Assigning a label is not mandatory but can help
        when aliasing resources. Some prefer to preload
        all needed resources and fetch them later by the label.
        This can he a lot less chaotic in larger applications.
        """
        return self._kwargs.get("label")

    @property
    def kind(self) -> str:
        """str: default resource kind.

        The resource ``kind`` is directly matched
        with the ``kind`` in loader classes.

        This property also supports assignment
        and is useful if the ``kind`` is detected
        based in the the attribute values.

        .. code:: python

            description.kind = 'something'
        """
        return self._kwargs.get("kind") or self.default_kind

    @kind.setter
    def kind(self, value) -> str:
        self._kwargs["kind"] = value

    @property
    def loader_cls(self) -> Type:
        """Type: The loader class for this resource.

        This property is assigned to during the loading
        stage were a loader class is assigned based on
        the `kind`.
        """
        return self._kwargs.get("loader_cls")

    @loader_cls.setter
    def loader_cls(self, value: Type):
        self._kwargs["loader_cls"] = value

    @property
    def resolved_path(self) -> Path:
        """pathlib.Path: The resolved path by a finder.

        The absolute path to the resource can optionally
        be assigned by a loader class.
        """
        return self._kwargs.get("resolved_path")

    @resolved_path.setter
    def resolved_path(self, value: Path):
        self._kwargs["resolved_path"] = value

    @property
    def attrs(self) -> Dict[str, str]:
        """dict: All keywords arguments passed to the resource"""
        return self._kwargs

    def __str__(self) -> str:
        return str(self._kwargs)

    def __repr__(self) -> str:
        return str(self)
