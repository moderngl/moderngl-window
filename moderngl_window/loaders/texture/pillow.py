from typing import Any

from PIL import Image

from moderngl_window.loaders.base import BaseLoader


class PillowLoader(BaseLoader):
    """Base loader using PIL/Pillow"""
    name = '__unknown__'

    def __init__(self, meta):
        super().__init__(meta)
        self.image = None

    def load(self) -> Any:
        raise NotImplementedError()

    def _open_image(self):
        if self.meta.image:
            self.image = self.meta.image
        else:
            self.meta.resolved_path = self.find_texture(self.meta.path)
            if not self.meta.resolved_path:
                raise ValueError("Cannot find texture: {}".format(self.meta.path))

            print("Loading:", self.meta.path)

            self.image = Image.open(self.meta.resolved_path)

        if self.meta.flip:
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)

    def _close_image(self):
        self.image.close()


def image_data(image):
    """Get components and bytes for an image"""
    # NOTE: We might want to check the actual image.mode
    #       and convert to an acceptable format.
    #       At the moment we load the data as is.
    data = image.tobytes()
    components = len(data) // (image.size[0] * image.size[1])
    return components, data
