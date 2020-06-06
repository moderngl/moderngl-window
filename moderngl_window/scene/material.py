import moderngl
from typing import Tuple


class MaterialTexture:
    """Wrapper for textures used in materials.
    Contains a texture and a sampler object.
    """
    def __init__(self, texture: moderngl.Texture = None, sampler: moderngl.Sampler = None):
        """Initialize instance.

        Args:
            texture (moderngl.Texture): Texture instance
            sampler (moderngl.Sampler): Sampler instance
        """
        self._texture = texture
        self._sampler = sampler

    @property
    def texture(self) -> moderngl.Texture:
        """moderngl.Texture: Texture instance"""
        return self._texture

    @texture.setter
    def texture(self, value):
        self._texture = value

    @property
    def sampler(self) -> moderngl.Sampler:
        """moderngl.Sampler: Sampler instance"""
        return self._sampler

    @sampler.setter
    def sampler(self, value):
        self._sampler = value


class Material:
    """Generic material"""
    def __init__(self, name: str = None):
        """Initialize material.

        Args:
            name (str): Name of the material
        """
        self._name = name or "default"
        self._color = (1.0, 1.0, 1.0, 1.0)
        self._mat_texture = None
        self._double_sided = True

    @property
    def name(self) -> str:
        """str: Name of the material"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def color(self) -> Tuple[float, float, float, float]:
        """Tuple[float, float, float, float]: RGBA color"""
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def mat_texture(self) -> MaterialTexture:
        """MaterialTexture: instance"""
        return self._mat_texture

    @mat_texture.setter
    def mat_texture(self, value):
        self._mat_texture = value

    @property
    def double_sided(self) -> bool:
        """bool: Material surface is double sided?"""
        return self._double_sided

    @double_sided.setter
    def double_sided(self, value):
        self._double_sided = value

    def release(self):
        if self._mat_texture:
            if self._mat_texture.texture:
                self._mat_texture.texture.release()

    def __str__(self) -> str:
        return "<Material {}>".format(self.name)

    def __repr__(self) -> str:
        return str(self)
