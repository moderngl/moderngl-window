from typing import Tuple
from PIL.Image import Image
from moderngl_window.meta.base import ResourceDescription


class TextureDescription(ResourceDescription):
    """Describes a texture to load"""
    default_kind = '2d'
    resource_type = 'textures'

    def __init__(self, path: str = None, kind: str = None, flip=True, mipmap=False,
                 mipmap_levels: Tuple[int, int] = None, anisotropy=16.0,
                 image=None, layers=None, **kwargs):
        """Describes a texture resource

        Args:
            path (str): path to resource relative to search directories
            flip (boolean): Flip the image horisontally
            mipmap (bool): Generate mipmaps
            mipmap_levels (tuple): (base, max_level) controlling mipmap generation.
                                   When defined the `mipmap` parameter is automatically `True`.
            anisotropy (float): Number of samples for anisotropic filtering
            kind (str): The kind of loader to use
            image: PIL image for when loading embedded resources
            layers: (int): Number of layers for texture arrays
        """
        kwargs.update({
            "path": path,
            "kind": kind,
            "flip": flip,
            "mipmap": mipmap,
            "mipmap_levels": mipmap_levels,
            "anisotropy": anisotropy,
            "layers": layers,
            "image": image,
        })
        super().__init__(**kwargs)

    @property
    def flip(self) -> bool:
        """bool: If the image should be flipped horisontally"""
        return self._kwargs.get('flip')

    @property
    def mipmap(self) -> bool:
        """bool: If mipmaps should be generated"""
        return self._kwargs.get('mipmap')

    @property
    def mipmap_levels(self) -> Tuple[int, int]:
        """Tuple[int, int]: base, max_level for mipmap generation"""
        return self._kwargs.get('mipmap_levels')

    @property
    def layers(self) -> int:
        """int: Number of layers in texture array"""
        return self._kwargs.get('layers')

    @property
    def anisotropy(self) -> float:
        """float: Number of samples for anisotropic filtering"""
        return self._kwargs.get('anisotropy')

    @property
    def image(self) -> Image:
        """Image: PIL image"""
        return self._kwargs.get('image')
