import moderngl

from moderngl_window.meta import ProgramDescription, ResourceDescription
from moderngl_window.resources.base import BaseRegistry


class Programs(BaseRegistry):
    """Handle program loading"""

    settings_attr = "PROGRAM_LOADERS"
    meta: ProgramDescription

    def resolve_loader(self, meta: ResourceDescription) -> None:
        """Resolve program loader.

        Determines if the references resource is a single
        or multiple glsl files unless ``kind`` is specified.

        Args:
            meta (ProgramDescription): The resource description
        """
        if meta.kind == "":
            if meta.path is None:
                meta.kind = "separate"
            else:
                meta.kind = "single"

        super().resolve_loader(meta)

    def load(self, meta: ResourceDescription) -> moderngl.Program:
        """Loads a shader program with the configured loaders

        Args:
            meta (:py:class:`~moderngl_window.meta.program.ProgramDescription`):
            The resource description
        Returns:
            moderngl.Program: The shader program
        """
        return super().load(meta)


programs = Programs()
