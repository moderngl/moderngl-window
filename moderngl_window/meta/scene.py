from moderngl_window.meta.base import ResourceDescription


class SceneDescription(ResourceDescription):
    """Describes a scene to load"""
    default_kind = None
    resource_type = 'scenes'

    def __init__(self, path=None, kind=None, cache=False, **kwargs):
        """Create a scene description
        Keyword Args:
            path (str): Path to resource
            kind (str): Loader kind
            cache (str): Use the loader caching system if present
        """
        kwargs.update({
            "path": path,
            "kind": kind,
            "cache": cache,
        })
        super().__init__(**kwargs)

    @property
    def cache(self):
        return self._kwargs['cache']
