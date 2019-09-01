import logging

import moderngl
from moderngl_window.loaders.base import BaseLoader
from moderngl_window.opengl import program
from moderngl_window.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)


class Loader(BaseLoader):
    kind = 'single'

    def load(self) -> moderngl.Program:
        """Loads a shader program from a single glsl file.

        Each shader type is separated by preprocessors

        - VERTEX_SHADER
        - FRAGMENT_SHADER
        - GEOMETRY_SHADER
        - TESS_CONTROL_SHADER
        - TESS_EVALUATION_SHADER

        Example:

        .. code:: glsl

            #version 330

            #if defined VERTEX_SHADER

            in vec3 in_position;
            in vec2 in_texcoord_0;
            out vec2 uv0;

            void main() {
                gl_Position = vec4(in_position, 1);
                uv0 = in_texcoord_0;
            }

            #elif defined FRAGMENT_SHADER

            out vec4 fragColor;
            uniform sampler2D texture0;
            in vec2 uv0;

            void main() {
                fragColor = texture(texture0, uv0);
            }
            #endif

        Returns:
            moderngl.Program: The Program instance
        """
        self.meta.resolved_path = self.find_program(self.meta.path)
        if not self.meta.resolved_path:
            raise ImproperlyConfigured("Cannot find program '{}'".format(self.meta.path))

        logger.info("Loading: %s", self.meta.path)

        with open(str(self.meta.resolved_path), 'r') as fd:
            shaders = program.ProgramShaders.from_single(self.meta, fd.read())

        prog = shaders.create()

        # Wrap the program if reloadable is set
        if self.meta.reloadable:
            # Disable reload flag so reloads will return Program instances
            self.meta.reloadable = False
            # Wrap it ..
            prog = program.ReloadableProgram(self.meta, prog)

        return prog
