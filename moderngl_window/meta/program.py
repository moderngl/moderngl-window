from typing import List
from moderngl_window.meta.base import ResourceDescription


class ProgramDescription(ResourceDescription):
    """Describes a program to load

    By default a program can be loaded in the following ways:

    - By supplying a `path` to s single glsl file containing all shaders
    - By supplying several paths to separate files containing each shader type.
      For example ``vertex_shader``, ``fragment_shader`` .. etc.

    .. code:: python

        # Single glsl file containing all shaders
        ProgramDescription(path='programs/myprogram.glsl')

        # Multiple shader files
        ProgramDescription(
            vertex_shader='programs/myprogram_vs.glsl'.
            fragment_shader='programs/myprogram_fs.glsl'.
            geometry_shader='programs/myprogram_gs.glsl'.
        )
    """

    default_kind = None
    resource_type = "programs"

    def __init__(
        self,
        path: str = None,
        kind: str = None,
        reloadable=False,
        vertex_shader: str = None,
        geometry_shader: str = None,
        fragment_shader: str = None,
        tess_control_shader: str = None,
        tess_evaluation_shader: str = None,
        compute_shader: str = None,
        defines: dict = None,
        varyings: List = None,
        **kwargs
    ):
        """Create a program description

        Keyword Args:
            path (str): path to the resource relative to search directories
            kind (str): The kind of loader to use
            reloadable (bool): Should this program be reloadable
            vertex_shader (str): Path to vertex shader file
            geometry_shader (str): Path to geometry shader
            fragment_shader (str): Path to fragmet shader
            tess_control_shader (str) Path to tess control shader
            tess_evaluation_shader (str): Path to tess eval shader
            compute_shader (str): Path to compute shader
            defines (dict): Dictionary with define values to replace in the source
            varyings (List): List of varying names for transform shader
            **kwargs: Optional custom attributes
        """
        kwargs.update(
            {
                "path": path,
                "kind": kind,
                "reloadable": reloadable,
                "vertex_shader": vertex_shader,
                "geometry_shader": geometry_shader,
                "fragment_shader": fragment_shader,
                "tess_control_shader": tess_control_shader,
                "tess_evaluation_shader": tess_evaluation_shader,
                "compute_shader": compute_shader,
                "defines": defines,
                "varyings": varyings,
            }
        )
        super().__init__(**kwargs)

    @property
    def reloadable(self) -> bool:
        """bool: if this program is reloadable"""
        return self._kwargs.get("reloadable")

    @reloadable.setter
    def reloadable(self, value):
        self._kwargs["reloadable"] = value

    @property
    def vertex_shader(self) -> str:
        """str: Relative path to vertex shader"""
        return self._kwargs.get("vertex_shader")

    @property
    def geometry_shader(self) -> str:
        """str: Relative path to geometry shader"""
        return self._kwargs.get("geometry_shader")

    @property
    def fragment_shader(self) -> str:
        """str: Relative path to fragment shader"""
        return self._kwargs.get("fragment_shader")

    @property
    def tess_control_shader(self) -> str:
        """str: Relative path to tess control shader"""
        return self._kwargs.get("tess_control_shader")

    @property
    def tess_evaluation_shader(self) -> str:
        """str: Relative path to tessellation evaluation shader"""
        return self._kwargs.get("tess_evaluation_shader")

    @property
    def compute_shader(self) -> str:
        """str: Relative path to compute shader"""
        return self._kwargs.get("compute_shader")

    @property
    def defines(self) -> dict:
        """dict: Dictionary with define values to replace in the source"""
        return self._kwargs.get("defines", {})

    @property
    def varyings(self) -> List:
        """List: List of varying names for transform shaders"""
        return self._kwargs.get("varyings", [])
