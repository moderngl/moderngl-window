from typing import Union

import logging
import moderngl
from moderngl_window.loaders.base import BaseLoader
from moderngl_window.opengl import program
from moderngl_window.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)


class Loader(BaseLoader):
    kind = 'separate'

    def load(self) -> Union[
        moderngl.Program,
        moderngl.ComputeShader,
        program.ReloadableProgram
    ]:
        """Loads a shader program were each shader is a separate file.

        This detected and dictated by the ``kind`` in the ``ProgramDescription``.

        Returns:
            moderngl.Program: The Program instance
        """
        prog = None

        vs_source = self.load_shader("vertex", self.meta.vertex_shader)
        geo_source = self.load_shader("geometry", self.meta.geometry_shader)
        fs_source = self.load_shader("fragment", self.meta.fragment_shader)
        tc_source = self.load_shader("tess_control", self.meta.tess_control_shader)
        te_source = self.load_shader("tess_evaluation", self.meta.tess_evaluation_shader)
        cs_source = self.load_shader("compute", self.meta.compute_shader)

        if vs_source and cs_source:
            raise ImproperlyConfigured("Cannot load program and compute shader simultaneously")

        if vs_source:
            shaders = program.ProgramShaders.from_separate(
                self.meta,
                vs_source,
                geometry_source=geo_source,
                fragment_source=fs_source,
                tess_control_source=tc_source,
                tess_evaluation_source=te_source,
            )
            prog = shaders.create()

            # Wrap the program if reloadable is set
            if self.meta.reloadable:
                # Disable reload flag so reloads will return Program instances
                self.meta.reloadable = False
                # Wrap it ..
                prog = program.ReloadableProgram(self.meta, prog)

        if cs_source:
            shaders = program.ProgramShaders.compute_shader(self.meta, cs_source)
            prog = shaders.create_compute_shader()

        return prog

    def load_shader(self, shader_type: str, path: str):
        """Load a single shader"""
        if path:
            resolved_path = self.find_program(path)
            if not resolved_path:
                raise ImproperlyConfigured("Cannot find {} shader '{}'".format(shader_type, path))

            logger.info("Loading: %s", resolved_path)

            with open(str(resolved_path), 'r') as fd:
                return fd.read()
