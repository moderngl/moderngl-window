"""
Helper classes for loading shader
"""
from typing import List, Tuple, Union

import moderngl
import moderngl_window
from moderngl_window.meta import ProgramDescription

VERTEX_SHADER = 'VERTEX_SHADER'
GEOMETRY_SHADER = 'GEOMETRY_SHADER'
FRAGMENT_SHADER = 'FRAGMENT_SHADER'
TESS_CONTROL_SHADER = 'TESS_CONTROL_SHADER'
TESS_EVALUATION_SHADER = 'TESS_EVALUATION_SHADER'
COMPUTE_SHADER = 'COMPUTE_SHADER'


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
    def from_separate(cls, meta: ProgramDescription, vertex_source, geometry_source=None, fragment_source=None,
                      tess_control_source=None, tess_evaluation_source=None):
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
    def compute_shader(cls, meta: ProgramDescription, compute_shader_source: str = None):
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
            geometry_shader=self.geometry_source.source if self.geometry_source else None,
            fragment_shader=self.fragment_source.source if self.fragment_source else None,
            tess_control_shader=self.tess_control_source.source if self.tess_control_source else None,
            tess_evaluation_shader=self.tess_evaluation_source.source if self.tess_evaluation_source else None,
            varyings=out_attribs,
        )
        program.extra = {'meta': self.meta}
        return program


class ShaderSource:
    """
    Helper class representing a single shader type
    """
    def __init__(self, shader_type: str, name: str, source: str, defines: dict = None):
        self.type = shader_type
        self.name = name
        self.source = source.strip()
        self.lines = self.source.split('\n')

        # Make sure version is present
        if not self.lines[0].startswith("#version"):
            self.print()
            raise ShaderError(
                "Missing #version in {}. A version must be defined in the first line".format(self.name),
            )

        self.apply_defines(defines)

        # Inject source with shade type
        self.lines.insert(1, "#define {} 1".format(self.type))
        self.lines.insert(2, "#line 2")

        self.source = '\n'.join(self.lines)

    def apply_defines(self, defines: dict):
        """Apply the configured define values"""
        if not defines:
            return

        for nr, line in enumerate(self.lines):
            line = line.strip()
            if line.startswith('#define'):
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
            if line.strip().startswith("out "):
                names.append(line.split()[2].replace(';', ''))

        return names

    def print(self):
        """Print the shader lines (for debugging)"""
        print("---[ START {} ]---".format(self.name))

        for i, line in enumerate(self.lines):
            print("{}: {}".format(str(i).zfill(3), line))

        print("---[ END {} ]---".format(self.name))


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

    def __getitem__(self, key) -> Union[moderngl.Uniform, moderngl.UniformBlock, moderngl.Subroutine,
                                        moderngl.Attribute, moderngl.Varying]:
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
        '''
            tuple: The subroutine uniforms.
        '''
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
        return '<ReloadableProgram: {} id={}>'.format(self.name, self.glo)
