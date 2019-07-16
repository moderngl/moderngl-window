from moderngl_window.meta.base import ResourceDescription


class SceneDescription(ResourceDescription):
    """Describes a scene to load"""
    default_kind = None
    resource_type = 'scenes'

    def __init__(self, path=None, kind=None, **kwargs):
        """Create a scene description
        Keyword Args:
            path (str): Path to resource
            kind (str): Loader kind
        """
        kwargs.update({
            "path": path,
            "kind": kind,
        })
        super().__init__(**kwargs)
