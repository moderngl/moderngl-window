import moderngl
from moderngl_window.resources.base import BaseRegistry
from moderngl_window.meta import ProgramDescription


class Programs(BaseRegistry):
    """Handle program loading"""

    settings_attr = "PROGRAM_LOADERS"

    def resolve_loader(self, meta: ProgramDescription) -> None:
        """Resolve program loader.

        Determines if the references resource is a single
        or multiple glsl files unless ``kind`` is specified.

        Args:
            meta (ProgramDescription): The resource description
        """
        if not meta.kind:
            meta.kind = "single" if meta.path else "separate"

        super().resolve_loader(meta)

    def load(self, meta: ProgramDescription) -> moderngl.Program:
        """Loads a shader program with the configured loaders

        Args:
            meta (:py:class:`~moderngl_window.meta.program.ProgramDescription`): The resource description
        Returns:
            moderngl.Program: The shader program
        """
        return super().load(meta)


programs = Programs()
