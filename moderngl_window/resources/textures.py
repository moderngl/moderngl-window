"""
Shader Registry
"""

from typing import Union
import moderngl
from moderngl_window.resources.base import BaseRegistry
from moderngl_window.meta import TextureDescription


class Textures(BaseRegistry):
    """Handles texture resources"""

    settings_attr = "TEXTURE_LOADERS"

    def load(self, meta: TextureDescription) -> Union[
        moderngl.Texture,
        moderngl.TextureArray,
        moderngl.TextureCube,
        moderngl.Texture3D,
    ]:
        """Loads a texture with the configured loaders.

        Args:
            meta (:py:class:`~moderngl_window.meta.texture.TextureDescription`):
            The resource description
        Returns:
            moderngl.Texture: 2d texture
        Returns:
            moderngl.TextureArray: texture array if ``layers`` is supplied
        """
        return super().load(meta)


textures = Textures()
