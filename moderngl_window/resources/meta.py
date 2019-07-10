from moderngl_window.resources.base import ResourceDescription


class DataDescription(ResourceDescription):
    """Describes data file to load"""
    default_kind = 'binary'
    resource_type = 'data'

    def __init__(self, path=None, kind=None, **kwargs):
        kwargs.update({
            "path": path,
            "kind": kind,
        })
        super().__init__(**kwargs)


class ProgramDescription(ResourceDescription):
    """Describes a program to load"""
    default_kind = None
    resource_type = 'programs'

    def __init__(self, path=None, kind=None, reloadable=False,
                 vertex_shader=None, geometry_shader=None, fragment_shader=None,
                 tess_control_shader=None, tess_evaluation_shader=None, **kwargs):
        kwargs.update({
            "path": path,
            "kind": kind,
            "reloadable": reloadable,
            "vertex_shader": vertex_shader,
            "geometry_shader": geometry_shader,
            "fragment_shader": fragment_shader,
            "tess_control_shader": tess_control_shader,
            "tess_evaluation_shader": tess_evaluation_shader,
        })
        super().__init__(**kwargs)

    @property
    def reloadable(self):
        return self._kwargs.get('reloadable')

    @reloadable.setter
    def reloadable(self, value):
        self._kwargs['reloadable'] = value

    @property
    def vertex_shader(self):
        return self._kwargs.get('vertex_shader')

    @property
    def geometry_shader(self):
        return self._kwargs.get('geometry_shader')

    @property
    def fragment_shader(self):
        return self._kwargs.get('fragment_shader')

    @property
    def tess_control_shader(self):
        return self._kwargs.get('tess_control_shader')

    @property
    def tess_evaluation_shader(self):
        return self._kwargs.get('tess_evaluation_shader')


class SceneDescription(ResourceDescription):
    """Describes a scene to load"""
    default_kind = None
    resource_type = 'scenes'

    def __init__(self, path=None, kind=None, **kwargs):
        kwargs.update({
            "path": path,
            "kind": kind,
        })
        super().__init__(**kwargs)


class TextureDescription(ResourceDescription):
    """Describes a texture to load"""
    default_kind = '2d'
    resource_type = 'textures'

    def __init__(self, path=None, flip=True, mipmap=True, kind=None, **kwargs):
        """Describes a texture resource

        Args:
            path (str): path to resource relative to search directories
            flip (boolean): Flip the image horisontally
            mipmap (bool): Generate mipmaps
        """
        kwargs.update({
            "path": path,
            "kind": kind,
            "flip": flip,
            "mipmap": mipmap,
        })
        super().__init__(**kwargs)

    @property
    def flip(self):
        return self._kwargs.get('flip')

    @property
    def image(self):
        return self._kwargs.get('image')

    @property
    def mipmap(self):
        return self._kwargs.get('mipmap')
