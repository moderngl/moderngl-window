from typing import Any, Optional

from moderngl_window.geometry.attributes import AttributeNames
from moderngl_window.meta.base import ResourceDescription


class SceneDescription(ResourceDescription):
    """Describes a scene to load.

    The correct loader is resolved by looking at the file extension.
    This can be overridden by specifying a ``kind`` that maps directly
    to a specific loader class.

    .. code:: python

        # Wavefront/obj file
        SceneDescription(path='scenes/cube.obj')

        # stl file
        SceneDescription(path='scenes/crater.stl')

        # GLTF 2 file
        SceneDescription(path='scenes/sponza.gltf')

    The user can also override what buffer/attribute names
    should be used by specifying ``attr_names``.

    A ``cache`` option is also available as some scene loaders
    supports converting the file into a different format
    on the fly to speed up loading.
    """

    default_kind = ""
    resource_type = "scenes"

    def __init__(
        self,
        path: Optional[str] = None,
        kind: Optional[str] = None,
        cache: bool = False,
        attr_names: type[AttributeNames] = AttributeNames,
        **kwargs: Any,
    ):
        """Create a scene description.

        Keyword Args:
            path (str): Path to resource
            kind (str): Loader kind
            cache (str): Use the loader caching system if present
            attr_names (AttributeNames): Attrib name config
            **kwargs: Optional custom attributes
        """
        if attr_names is None:
            attr_names = AttributeNames

        kwargs.update({"path": path, "kind": kind, "cache": cache, "attr_names": attr_names})
        super().__init__(**kwargs)

    @property
    def cache(self) -> bool:
        """bool: Use cache feature in scene loader"""
        return bool(self._kwargs["cache"])

    @property
    def attr_names(self) -> AttributeNames:
        """AttributeNames: Attribute name config"""
        return self._kwargs["attr_names"]
