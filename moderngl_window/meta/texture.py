from typing import Any, Optional

from PIL.Image import Image

from moderngl_window.meta.base import ResourceDescription


class TextureDescription(ResourceDescription):
    """Describes a texture to load.

    Example:

    .. code:: python

        # Loading a 2d texture
        TextureDescription(path='textures/wood.png')

        # Loading a 2d texture with mimpmaps with anisotropy
        TextureDescription(path='textures/wood.png', mipmap=True, anisotropy=16.0)

        # Loading texture array containing 10 layers
        TextureDescription(path='textures/tiles.png', layers=10, kind='array')
    """

    default_kind = "2d"
    resource_type = "textures"

    def __init__(
        self,
        path: Optional[str] = None,
        kind: Optional[str] = None,
        flip: bool = True,
        flip_x: bool = False,
        flip_y: bool = True,
        mipmap: bool = False,
        mipmap_levels: Optional[tuple[int, int]] = None,
        anisotropy: float =1.0,
        image: Optional[Image] = None,
        layers: Optional[int] = None,
        pos_x: Optional[str] = None,
        pos_y: Optional[str] = None,
        pos_z: Optional[str] = None,
        neg_x: Optional[str] = None,
        neg_y: Optional[str] = None,
        neg_z: Optional[str] = None,
        **kwargs: Any,
    ):
        """Describes a texture resource

        Args:
            path (str): path to resource relative to search directories
            kind (str): The kind of loader to use
            flip (boolean): (use flip_y) Flip the image vertically (top to bottom)
            flip_x (boolean): Flip the image horizontally (left to right)
            flip_y (boolean): Flip the image vertically (top to bottom)
            mipmap (bool): Generate mipmaps. Will generate max possible levels unless
                           `mipmap_levels` is defined.
            mipmap_levels (tuple): (base, max_level) controlling mipmap generation.
                                   When defined the `mipmap` parameter is automatically `True`.
            anisotropy (float): Number of samples for anisotropic filtering
            image: PIL image for when loading embedded resources
            layers: (int): Number of layers for texture arrays
            neg_x (str): Path to negative x texture in a cube map
            neg_y (str): Path to negative y texture in a cube map
            neg_z (str): Path to negative z texture in a cube map
            pos_x (str): Path to positive x texture in a cube map
            pop_y (str): Path to positive y texture in a cube map
            pos_z (str): Path to positive z texture in a cube map
            **kwargs: Any optional/custom attributes
        """
        kwargs.update(
            {
                "path": path,
                "kind": kind,
                "flip_x": flip_x,
                "flip_y": flip and flip_y,
                "mipmap": mipmap,
                "mipmap_levels": mipmap_levels,
                "anisotropy": anisotropy,
                "layers": layers,
                "image": image,
                "neg_x": neg_x,
                "neg_y": neg_y,
                "neg_z": neg_z,
                "pos_x": pos_x,
                "pos_y": pos_y,
                "pos_z": pos_z,
            }
        )
        super().__init__(**kwargs)

    @property
    def flip_x(self) -> Optional[bool]:
        """bool: If the image should be flipped horizontally (left to right)"""
        return self._kwargs.get("flip_x")

    @property
    def flip_y(self) -> Optional[bool]:
        """bool: If the image should be flipped vertically (top to bottom)"""
        return self._kwargs.get("flip_y")

    @property
    def mipmap(self) -> Optional[bool]:
        """bool: If mipmaps should be generated"""
        return self._kwargs.get("mipmap")

    @mipmap.setter
    def mipmap(self, value: float) -> None:
        self._kwargs["mipmap"] = value

    @property
    def mipmap_levels(self) -> Optional[tuple[int, int]]:
        """tuple[int, int]: base, max_level for mipmap generation"""
        return self._kwargs.get("mipmap_levels")

    @property
    def layers(self) -> Optional[int]:
        """int: Number of layers in texture array"""
        return self._kwargs.get("layers")

    @property
    def anisotropy(self) -> Optional[float]:
        """float: Number of samples for anisotropic filtering"""
        return self._kwargs.get("anisotropy")

    @property
    def image(self) -> Optional[Image]:
        """Image: PIL image when loading embedded resources"""
        return self._kwargs.get("image")

    @property
    def pos_x(self) -> Optional[str]:
        """str: Path to positive x in a cubemap texture"""
        return self._kwargs.get("pos_x")

    @property
    def pos_y(self) -> Optional[str]:
        """str: Path to positive y in a cubemap texture"""
        return self._kwargs.get("pos_y")

    @property
    def pos_z(self) -> Optional[str]:
        """str: Path to positive z in a cubemap texture"""
        return self._kwargs.get("pos_z")

    @property
    def neg_x(self) -> Optional[str]:
        """str: Path to negative x in a cubemap texture"""
        return self._kwargs.get("neg_x")

    @property
    def neg_y(self) -> Optional[str]:
        """str: Path to negative y in a cubemap texture"""
        return self._kwargs.get("neg_y")

    @property
    def neg_z(self) -> Optional[str]:
        """str: Path to negative z in a cubemap texture"""
        return self._kwargs.get("neg_z")
