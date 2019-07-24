from moderngl_window.loaders.texture.pillow import PillowLoader, image_data
from moderngl_window.exceptions import ImproperlyConfigured


class Loader(PillowLoader):
    kind = 'array'

    def __init__(self, meta):
        super().__init__(meta)
        self.layers = self.meta.layers

        if self.layers is None:
            raise ImproperlyConfigured("TextureArray requires layers parameter")

    def load(self):
        """Load a texture array"""
        self._open_image()

        width, height, depth = self.image.size[0], self.image.size[1] // self.layers, self.layers
        components, data = image_data(self.image)

        texture = self.ctx.texture_array(
            (width, height, depth),
            components,
            data,
        )
        texture.extra = {'meta': self.meta}

        if self.meta.mipmap:
            texture.build_mipmaps()

        self._close_image()

        return texture
