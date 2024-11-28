from typing import Optional

import moderngl


class MaterialTexture:
    """Wrapper for textures used in materials.
    Contains a texture and a sampler object.
    """

    def __init__(
        self, texture: Optional[moderngl.Texture] = None, sampler: Optional[moderngl.Sampler] = None
    ):
        """Initialize instance.

        Args:
            texture (moderngl.Texture): Texture instance
            sampler (moderngl.Sampler): Sampler instance
        """
        self._texture = texture
        self._sampler = sampler

    @property
    def texture(self) -> Optional[moderngl.Texture]:
        """moderngl.Texture: Texture instance"""
        return self._texture

    @texture.setter
    def texture(self, value: moderngl.Texture) -> None:
        self._texture = value

    @property
    def sampler(self) -> Optional[moderngl.Sampler]:
        """moderngl.Sampler: Sampler instance"""
        return self._sampler

    @sampler.setter
    def sampler(self, value: moderngl.Sampler) -> None:
        self._sampler = value


class Material:
    """Generic material"""

    def __init__(self, name: str = ""):
        """Initialize material.

        Args:
            name (str): Name of the material
        """
        self._name = name or "default"
        self._color = (1.0, 1.0, 1.0, 1.0)
        self._mat_texture: Optional[MaterialTexture] = None
        self._double_sided = True

    @property
    def name(self) -> str:
        """str: Name of the material"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def color(self) -> tuple[float, float, float, float]:
        """tuple[float, float, float, float]: RGBA color"""
        return self._color

    @color.setter
    def color(self, value: tuple[float, float, float, float]) -> None:
        self._color = value

    @property
    def mat_texture(self) -> Optional[MaterialTexture]:
        """MaterialTexture: instance"""
        return self._mat_texture

    @mat_texture.setter
    def mat_texture(self, value: MaterialTexture) -> None:
        self._mat_texture = value

    @property
    def double_sided(self) -> bool:
        """bool: Material surface is double sided?"""
        return self._double_sided

    @double_sided.setter
    def double_sided(self, value: bool) -> None:
        self._double_sided = value

    def release(self) -> None:
        if self._mat_texture:
            if self._mat_texture.texture:
                self._mat_texture.texture.release()

    def __str__(self) -> str:
        return "<Material {}>".format(self.name)

    def __repr__(self) -> str:
        return str(self)
