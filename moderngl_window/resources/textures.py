"""
Shader Registry
"""

from typing import Union

import moderngl

from moderngl_window.meta import ResourceDescription, TextureDescription
from moderngl_window.resources.base import BaseRegistry

TextureAny = Union[
    moderngl.Texture,
    moderngl.TextureArray,
    moderngl.TextureCube,
    moderngl.Texture3D,
]


class Textures(BaseRegistry):
    """Handles texture resources"""

    settings_attr = "TEXTURE_LOADERS"
    meta: TextureDescription

    def load(self, meta: ResourceDescription) -> TextureAny:
        """Loads a texture with the configured loaders.

        Args:
            meta (:py:class:`~moderngl_window.meta.texture.TextureDescription`):
            The resource description
        Returns:
            moderngl.Texture: 2d texture
        Returns:
            moderngl.TextureArray: texture array if ``layers`` is supplied
        """
        texture = super().load(meta)
        assert (
            isinstance(texture, moderngl.Texture)
            or isinstance(texture, moderngl.TextureArray)
            or isinstance(texture, moderngl.TextureCube)
            or isinstance(texture, moderngl.Texture3D)
        ), f"{meta} did not load a texture. Please correct it"
        return texture


textures = Textures()
