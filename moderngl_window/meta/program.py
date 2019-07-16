from moderngl_window.meta.base import ResourceDescription


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
