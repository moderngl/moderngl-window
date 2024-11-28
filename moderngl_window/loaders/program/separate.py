import logging
from pathlib import Path
from typing import Optional, Union

import moderngl

from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.loaders.base import BaseLoader
from moderngl_window.opengl import program

logger = logging.getLogger(__name__)


class Loader(BaseLoader):
    kind = "separate"
    meta: program.ProgramDescription

    def load(
        self,
    ) -> Union[moderngl.Program, moderngl.ComputeShader, program.ReloadableProgram]:
        """Loads a shader program were each shader is a separate file.

        This detected and dictated by the ``kind`` in the ``ProgramDescription``.

        Returns:
            moderngl.Program: The Program instance
        """
        prog: Union[moderngl.Program, moderngl.ComputeShader, program.ReloadableProgram]

        vs_source = self._load_shader("vertex", self.meta.vertex_shader)
        geo_source = self._load_shader("geometry", self.meta.geometry_shader)
        fs_source = self._load_shader("fragment", self.meta.fragment_shader)
        tc_source = self._load_shader("tess_control", self.meta.tess_control_shader)
        te_source = self._load_shader("tess_evaluation", self.meta.tess_evaluation_shader)
        cs_source = self._load_shader("compute", self.meta.compute_shader)

        if vs_source:
            shaders = program.ProgramShaders.from_separate(
                self.meta,
                vs_source,
                geometry_source=geo_source,
                fragment_source=fs_source,
                tess_control_source=tc_source,
                tess_evaluation_source=te_source,
            )
            shaders.handle_includes(self._load_source)
            prog = shaders.create()

            # Wrap the program if reloadable is set
            if self.meta.reloadable:
                # Disable reload flag so reloads will return Program instances
                self.meta.reloadable = False
                # Wrap it ..
                prog = program.ReloadableProgram(self.meta, prog)
        elif cs_source:
            shaders = program.ProgramShaders.compute_shader(self.meta, cs_source)
            shaders.handle_includes(self._load_source)
            prog = shaders.create_compute_shader()
        else:
            raise ImproperlyConfigured("Cannot find a shader source to load")

        return prog

    def _load_shader(self, shader_type: str, path: Optional[str]) -> Optional[str]:
        """Load a single shader source"""
        if path is not None:
            resolved_path = self.find_program(path)
            if not resolved_path:
                raise ImproperlyConfigured("Cannot find {} shader '{}'".format(shader_type, path))

            logger.info("Loading: %s", resolved_path)

            with open(str(resolved_path), "r") as fd:
                return fd.read()
        return None

    def _load_source(self, path: Union[Path, str]) -> tuple[Path, str]:
        """Finds and loads a single source file.

        Args:
            path: Path to resource
        Returns:
            tuple[resolved_path, source]: The resolved path and the source
        """
        resolved_path = self.find_program(path)
        if resolved_path is None:
            raise ImproperlyConfigured("Cannot find program '{}'".format(path))

        logger.info("Loading: %s", path)

        with open(str(resolved_path), "r") as fd:
            return resolved_path, fd.read()
