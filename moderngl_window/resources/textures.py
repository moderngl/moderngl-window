"""
Shader Registry
"""
from typing import Union
import moderngl
from moderngl_window.resources.base import BaseRegistry
from moderngl_window.meta import TextureDescription


class Textures(BaseRegistry):
    """
    A registry for textures requested by effects.
    Once all effects are initialized, we ask this class to load the textures.
    """
    settings_attr = 'TEXTURE_LOADERS'

    def load(self, meta: TextureDescription) -> Union[moderngl.Texture, moderngl.Texture3D,
                                                      moderngl.TextureArray, moderngl.TextureCube]:
        """Loads a texture with the configured loaders"""
        return super().load(meta)


textures = Textures()
