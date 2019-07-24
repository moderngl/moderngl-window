import logging

import moderngl
from moderngl_window.loaders.base import BaseLoader
from moderngl_window.opengl import program
from moderngl_window.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)


class Loader(BaseLoader):
    kind = 'single'

    def load(self) -> moderngl.Program:
        self.meta.resolved_path = self.find_program(self.meta.path)
        if not self.meta.resolved_path:
            raise ImproperlyConfigured("Cannot find program '{}'".format(self.meta.path))

        logger.info("Loading: %s", self.meta.path)

        with open(self.meta.resolved_path, 'r') as fd:
            shaders = program.ProgramShaders.from_single(self.meta, fd.read())

        prog = shaders.create()

        # Wrap the program if reloadable is set
        if self.meta.reloadable:
            # Disable reload flag so reloads will return Program instances
            self.meta.reloadable = False
            # Wrap it ..
            prog = program.ReloadableProgram(self.meta, prog)

        return prog
