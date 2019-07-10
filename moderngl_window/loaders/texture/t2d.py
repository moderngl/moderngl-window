from moderngl_window.loaders.texture.pillow import PillowLoader, image_data


class Loader(PillowLoader):
    kind = '2d'

    def load(self):
        """Load a 2d texture"""
        self._open_image()

        components, data = image_data(self.image)

        texture = self.ctx.texture(
            self.image.size,
            components,
            data,
        )
        texture.extra = {'meta': self.meta}

        if self.meta.mipmap:
            texture.build_mipmaps()

        self._close_image()

        return texture
