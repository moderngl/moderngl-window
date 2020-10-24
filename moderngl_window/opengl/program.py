"""
Helper classes for loading shader
"""
from typing import List, Tuple, Union
import re

import moderngl
import moderngl_window
from moderngl_window.meta import ProgramDescription

VERTEX_SHADER = "VERTEX_SHADER"
GEOMETRY_SHADER = "GEOMETRY_SHADER"
FRAGMENT_SHADER = "FRAGMENT_SHADER"
TESS_CONTROL_SHADER = "TESS_CONTROL_SHADER"
TESS_EVALUATION_SHADER = "TESS_EVALUATION_SHADER"
COMPUTE_SHADER = "COMPUTE_SHADER"


class ProgramShaders:
    """Helper class preparing shader source strings for a program"""

    def __init__(self, meta: ProgramDescription):
        self.meta = meta
        self.vertex_source = None
        self.geometry_source = None
        self.fragment_source = None
        self.tess_control_source = None
        self.tess_evaluation_source = None
        self.compute_shader_source = None

    @property
    def ctx(self) -> moderngl.Context:
        """The moderngl context"""
        return moderngl_window.ctx()

    @classmethod
    def from_single(cls, meta: ProgramDescription, source: str):
        """Initialize a single glsl string containing all shaders"""
        instance = cls(meta)
        instance.vertex_source = ShaderSource(
            VERTEX_SHADER,
            meta.path or meta.vertex_shader,
            source,
            defines=meta.defines,
        )

        if GEOMETRY_SHADER in source:
            instance.geometry_source = ShaderSource(
                GEOMETRY_SHADER,
                meta.path or meta.geometry_shader,
                source,
                defines=meta.defines,
            )

        if FRAGMENT_SHADER in source:
            instance.fragment_source = ShaderSource(
                FRAGMENT_SHADER,
                meta.path or meta.fragment_shader,
                source,
                defines=meta.defines,
            )

        if TESS_CONTROL_SHADER in source:
            instance.tess_control_source = ShaderSource(
                TESS_CONTROL_SHADER,
                meta.path or meta.tess_control_shader,
                source,
                defines=meta.defines,
            )

        if TESS_EVALUATION_SHADER in source:
            instance.tess_evaluation_source = ShaderSource(
                TESS_EVALUATION_SHADER,
                meta.path or meta.tess_evaluation_shader,
                source,
                defines=meta.defines,
            )

        return instance

    @classmethod
    def from_separate(
        cls,
        meta: ProgramDescription,
        vertex_source,
        geometry_source=None,
        fragment_source=None,
        tess_control_source=None,
        tess_evaluation_source=None,
    ):
        """Initialize multiple shader strings"""
        instance = cls(meta)
        instance.vertex_source = ShaderSource(
            VERTEX_SHADER,
            meta.path or meta.vertex_shader,
            vertex_source,
            defines=meta.defines,
        )

        if geometry_source:
            instance.geometry_source = ShaderSource(
                GEOMETRY_SHADER,
                meta.path or meta.geometry_shader,
                geometry_source,
                defines=meta.defines,
            )

        if fragment_source:
            instance.fragment_source = ShaderSource(
                FRAGMENT_SHADER,
                meta.path or meta.fragment_shader,
                fragment_source,
                defines=meta.defines,
            )

        if tess_control_source:
            instance.tess_control_source = ShaderSource(
                TESS_CONTROL_SHADER,
                meta.path or meta.tess_control_shader,
                tess_control_source,
                defines=meta.defines,
            )

        if tess_evaluation_source:
            instance.tess_evaluation_source = ShaderSource(
                TESS_EVALUATION_SHADER,
                meta.path or meta.tess_control_shader,
                tess_evaluation_source,
                defines=meta.defines,
            )

        return instance

    @classmethod
    def compute_shader(
        cls, meta: ProgramDescription, compute_shader_source: str = None
    ):
        instance = cls(meta)
        instance.compute_shader_source = ShaderSource(
            COMPUTE_SHADER,
            meta.compute_shader,
            compute_shader_source,
            defines=meta.defines,
        )
        return instance

    def create_compute_shader(self):
        return self.ctx.compute_shader(self.compute_shader_source.source)

    def create(self):
        """
        Creates a shader program.

        Returns:
            ModernGL Program instance
        """
        # Get out varyings
        out_attribs = []

        # If no fragment shader is present we are doing transform feedback
        if not self.fragment_source:
            # Out attributes is present in geometry shader if present
            if self.geometry_source:
                out_attribs = self.geometry_source.find_out_attribs()
            # Otherwise they are specified in vertex shader
            else:
                out_attribs = self.vertex_source.find_out_attribs()

        program = self.ctx.program(
            vertex_shader=self.vertex_source.source,
            geometry_shader=self.geometry_source.source
            if self.geometry_source
            else None,
            fragment_shader=self.fragment_source.source
            if self.fragment_source
            else None,
            tess_control_shader=self.tess_control_source.source
            if self.tess_control_source
            else None,
            tess_evaluation_shader=self.tess_evaluation_source.source
            if self.tess_evaluation_source
            else None,
            varyings=out_attribs,
        )
        program.extra = {"meta": self.meta}
        return program

    def handle_includes(self, load_source_func):
        """Resolves ``#include`` preprocessors

        Args:
            load_source_func (func): A function for finding and loading a source
        """
        if self.vertex_source:
            self.vertex_source.handle_includes(load_source_func)
        if self.geometry_source:
            self.geometry_source.handle_includes(load_source_func)
        if self.fragment_source:
            self.fragment_source.handle_includes(load_source_func)
        if self.tess_control_source:
            self.tess_control_source.handle_includes(load_source_func)
        if self.tess_evaluation_source:
            self.tess_evaluation_source.handle_includes(load_source_func)
        if self.compute_shader_source:
            self.compute_shader_source.handle_includes(load_source_func)


class ShaderSource:
    """
    Helper class representing a single shader type.

    It ensures the source has the right format, injects ``#define`` preprocessors,
    resolves ``#include`` preprocessors etc.

    A ``ShaderSource`` can be the base/root shader or a source referenced in an ``#include``.
    """

    def __init__(
        self,
        shader_type: str,
        name: str,
        source: str,
        defines: dict = None,
        id=0,
        root=True,
    ):
        """Create shader source.

        Args:
            shader_type (str): A preprocessor name for setting the shader type
            name (str): A string (usually the path) so we can give useful error messages to the user
            source (str): The raw source for the shader
        Keyword Args:
            id (int): The source number. Used when shader consists of multiple sources through includes
            root (bool): If this shader source is the root shader (Not an include)
        """
        self._id = id
        self._root = root
        self._source_list = [
            self
        ]  # List of sources this shader consists of (original source + includes)
        self._type = shader_type
        self._name = name
        self._defines = defines or {}
        if root:
            source = source.strip()
        self._lines = source.split("\n")

        # Make sure version is present (only if root shader)
        if self._root and not self._lines[0].startswith("#version"):
            self.print()
            raise ShaderError(
                "Missing #version in {}. A version must be defined in the first line".format(
                    self._name
                ),
            )

        self.apply_defines(defines)

        # Inject source with shade type
        if self._root:
            self._lines.insert(1, "#define {} 1".format(self._type))
            self._lines.insert(2, "#line 2")

    @property
    def id(self) -> int:
        """int: The shader number/id"""
        return self._id

    @property
    def source(self) -> str:
        """str: The source lines as a string"""
        return "\n".join(self._lines)

    @property
    def source_list(self) -> List["ShaderSource"]:
        """List[ShaderSource]: List of all shader sources"""
        return self._source_list

    @property
    def name(self) -> str:
        """str: a path or name for this shader"""
        return self._name

    @property
    def lines(self) -> List[str]:
        """List[str]: The lines in this shader"""
        return self._lines

    @property
    def line_count(self) -> int:
        """int: Number of lines in this source (stripped)"""
        return len(self._lines)

    @property
    def defines(self) -> dict:
        """dict: Defines configured for this shader"""
        return self._defines

    def handle_includes(self, load_source_func, depth=0, source_id=0):
        """Inject includes into the shader source.
        This happens recursively up to a max level in case the users has circular includes.
        We also build up a list of all the included sources in the root shader.

        Args:
            load_source_func (func): A function for finding and loading a source
            depth (int): The current include depth (incease by 1 for every call)
        """
        if depth > 100:
            raise ShaderError(
                "Reaching an include depth of 100. You probably have circular includes"
            )

        current_id = source_id
        while True:
            for nr, line in enumerate(self._lines):
                line = line.strip()
                if line.startswith("#include"):
                    path = line[9:]
                    current_id += 1
                    _, source = load_source_func(path)
                    source = ShaderSource(
                        None,
                        path,
                        source,
                        defines=self._defines,
                        id=current_id,
                        root=False,
                    )
                    source.handle_includes(
                        load_source_func, depth=depth + 1, source_id=current_id
                    )
                    self._lines = self.lines[:nr] + source.lines + self.lines[nr + 1:]
                    self._source_list += source.source_list
                    current_id = self._source_list[-1].id
                    break
            else:
                break

    def apply_defines(self, defines: dict):
        """Apply the configured define values"""
        if not defines:
            return

        for nr, line in enumerate(self._lines):
            line = line.strip()
            if line.startswith("#define"):
                try:
                    name = line.split()[1]
                    value = defines.get(name)
                    if not value:
                        continue

                    self.lines[nr] = "#define {} {}".format(name, str(value))
                except IndexError:
                    pass

    def find_out_attribs(self) -> List[str]:
        """
        Get all out attributes in the shader source.

        Returns:
            List[str]: List of out attribute names
        """
        names = []
        for line in self.lines:
            res = re.match(
                r"(layout(.+)\))?(\s+)?(out)(\s+)(\w+)(\s+)(\w+)", line.strip()
            )
            if res:
                names.append(res.groups()[-1])

        return names

    def print(self):
        """Print the shader lines (for debugging)"""
        print("---[ START {} ]---".format(self.name))

        for i, line in enumerate(self.lines):
            print("{}: {}".format(str(i).zfill(3), line))

        print("---[ END {} ]---".format(self.name))

    def __repr__(self):
        return "<ShaderSource: {} id={}>".format(self.name, self.id)


class ShaderError(Exception):
    pass


class ReloadableProgram:
    """
    Programs we want to be reloadable must be created with this wrapper.
    """

    def __init__(self, meta: ProgramDescription, program: moderngl.Program):
        """
        Create a shader using either a file path or a name.

        Args:
            meta: The program meta
            program: The program instance
        """
        self.program = program
        self.meta = meta

    @property
    def name(self):
        return self.meta.path or self.meta.vertex_shader

    @property
    def _members(self):
        return self.program._members

    @property
    def ctx(self) -> moderngl.Context:
        return self.program.ctx

    def __getitem__(
        self, key
    ) -> Union[
        moderngl.Uniform,
        moderngl.UniformBlock,
        moderngl.Subroutine,
        moderngl.Attribute,
        moderngl.Varying,
    ]:
        return self.program[key]

    def get(self, key, default):
        return self.program.get(key, default)

    @property
    def extra(self):
        return self.program.extra

    @property
    def mglo(self):
        """The ModernGL Program object"""
        return self.program.mglo

    @property
    def glo(self) -> int:
        """
        int: The internal OpenGL object.
        This values is provided for debug purposes only.
        """
        return self.program.glo

    @property
    def subroutines(self) -> Tuple[str, ...]:
        """
            tuple: The subroutine uniforms.
        """
        return self.program.subroutines

    @property
    def geometry_input(self) -> int:
        """
        int: The geometry input primitive.
        The GeometryShader's input primitive if the GeometryShader exists.
        The geometry input primitive will be used for validation.
        """
        return self.program.geometry_input

    @property
    def geometry_output(self) -> int:
        """
        int: The geometry output primitive.
        The GeometryShader's output primitive if the GeometryShader exists.
        """
        return self.program.geometry_output

    @property
    def geometry_vertices(self) -> int:
        """
        int: The maximum number of vertices that
        the geometry shader will output.
        """
        return self.program.geometry_vertices

    def __repr__(self):
        return "<ReloadableProgram: {} id={}>".format(self.name, self.glo)
