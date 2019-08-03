from moderngl_window.meta.base import ResourceDescription
from moderngl_window.geometry.attributes import AttributeNames


class SceneDescription(ResourceDescription):
    """Describes a scene to load"""
    default_kind = None
    resource_type = 'scenes'

    def __init__(self, path=None, kind=None, cache=False, attr_names=AttributeNames, **kwargs):
        """Create a scene description
        Keyword Args:
            path (str): Path to resource
            kind (str): Loader kind
            cache (str): Use the loader caching system if present
            attr_names (AttributeNames): Attrib name config
        """
        kwargs.update({
            "path": path,
            "kind": kind,
            "cache": cache,
            "attr_names": attr_names,
        })
        super().__init__(**kwargs)

    @property
    def cache(self) -> bool:
        """bool: Use cache feature in scene loader"""
        return self._kwargs['cache']

    @property
    def attr_names(self) -> AttributeNames:
        """AttributeNames: Attribute name config"""
        return self._kwargs['attr_names']
