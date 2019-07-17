from moderngl_window.meta.base import ResourceDescription


class DataDescription(ResourceDescription):
    """Describes data file to load"""
    default_kind = None
    resource_type = 'data'

    def __init__(self, path=None, kind=None, **kwargs):
        kwargs.update({
            "path": path,
            "kind": kind,
        })
        super().__init__(**kwargs)
