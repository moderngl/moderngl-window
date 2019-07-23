from moderngl_window.meta.base import ResourceDescription


class TextureDescription(ResourceDescription):
    """Describes a texture to load"""
    default_kind = '2d'
    resource_type = 'textures'

    def __init__(self, path: str = None, kind: str = None, flip=True, mipmap=True,
                 image=None, layers=None, **kwargs):
        """Describes a texture resource

        Args:
            path (str): path to resource relative to search directories
            flip (boolean): Flip the image horisontally
            mipmap (bool): Generate mipmaps
            kind (str): The kind of loader to use
            image: PIL image when loading embedded resources
            layers: (int): Number of layers for texture arrays
        """
        kwargs.update({
            "path": path,
            "kind": kind,
            "flip": flip,
            "mipmap": mipmap,
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
    def layers(self) -> int:
        """Number of layers in texture array"""
        return self._kwargs.get('layers')

    @property
    def image(self):
        """PIL image"""
        return self._kwargs.get('image')
