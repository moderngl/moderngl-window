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

    def __init__(self, path: str = None, kind: str = None, reloadable=False,
                 vertex_shader: str = None, geometry_shader: str = None, fragment_shader: str = None,
                 tess_control_shader: str = None, tess_evaluation_shader: str = None, **kwargs):
        """Create a program description

        Keyword Args:
            path (str): path to the resource realive to search directories
            kind (str): The kind of loader to use
            reloadable (bool): Should this program be reloadable
            vertex_shader (str): Path to vertex shader file
            geometry_shader (str): Path to geometry shader
            fragment_shader (str): Path to fragmet shader
            tess_control_shader (str) Path to tess control shader
            tess_evaluation_shader (str): Path to tess eval shader
        """
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
        """bool: if this program is reloadable"""
        return self._kwargs.get('reloadable')

    @reloadable.setter
    def reloadable(self, value):
        self._kwargs['reloadable'] = value

    @property
    def vertex_shader(self):
        """str: path to vertex shader"""
        return self._kwargs.get('vertex_shader')

    @property
    def geometry_shader(self):
        """str: path to geometry shader"""
        return self._kwargs.get('geometry_shader')

    @property
    def fragment_shader(self):
        """str: path to fragment shader"""
        return self._kwargs.get('fragment_shader')

    @property
    def tess_control_shader(self):
        """str: path to tess control shader"""
        return self._kwargs.get('tess_control_shader')

    @property
    def tess_evaluation_shader(self):
        """str: path to tese eval shader"""
        return self._kwargs.get('tess_evaluation_shader')


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


class TextureDescription(ResourceDescription):
    """Describes a texture to load"""
    default_kind = '2d'
    resource_type = 'textures'

    def __init__(self, path: str = None, kind: str = None, flip=True, mipmap=True, **kwargs):
        """Describes a texture resource

        Args:
            path (str): path to resource relative to search directories
            flip (boolean): Flip the image horisontally
            mipmap (bool): Generate mipmaps
            kind (str): The kind of loader to use
        """
        kwargs.update({
            "path": path,
            "kind": kind,
            "flip": flip,
            "mipmap": mipmap,
        })
        super().__init__(**kwargs)

    @property
    def flip(self) -> bool:
        """bool: If the image should be flipped horisontally"""
        return self._kwargs.get('flip')

    @property
    def mipmap(self) -> bool:
        """bool: If mipmaps should be generated"""
        return self._kwargs.get('mipmap')
