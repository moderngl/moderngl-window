import logging
from pathlib import Path
from typing import Optional, Union

try:
    from PIL import Image
except ImportError as ex:
    raise ImportError("Texture loader 'PillowLoader' requires Pillow: {}".format(ex))

from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.loaders.base import BaseLoader
from moderngl_window.meta.base import ResourceDescription
from moderngl_window.meta.texture import TextureDescription
from moderngl_window.resources.textures import TextureAny

logger = logging.getLogger(__name__)


class PillowLoader(BaseLoader):
    """Base loader using PIL/Pillow"""

    kind = "__unknown__"
    image: Image.Image
    meta: TextureDescription

    def __init__(self, meta: ResourceDescription):
        super().__init__(meta)

    def load(self) -> TextureAny:
        raise NotImplementedError()

    def _open_image(self) -> Image.Image:
        if self.meta.image:
            self.image = self.meta.image
        else:
            self.meta.resolved_path = self.find_texture(self.meta.path)
            logger.info("loading %s", self.meta.resolved_path)
            if not self.meta.resolved_path:
                raise ImproperlyConfigured("Cannot find texture: {}".format(self.meta.path))

            self.image = Image.open(self.meta.resolved_path)

            # If the image is animated (like a gif anim) we convert it into a vertical strip
            if (
                hasattr(self.image, "is_animated")
                and self.image.is_animated
                and hasattr(self.image, "n_frames")
            ):
                self.layers = self.image.n_frames
                anim = Image.new(
                    self.image.palette.mode if self.image.palette is not None else "L",
                    (self.image.width, self.image.height * self.image.n_frames),
                )
                anim.putalpha(0)

                for frame_number in range(self.image.n_frames):
                    self.image.seek(frame_number)
                    frame = self._palette_to_raw(self.image, mode="RGBA")
                    anim.paste(frame, (0, frame_number * self.image.height))

                self.image = anim

        self.image = self._apply_modifiers(self.image)
        return self.image

    def _load_texture(self, path: Union[str, Path]) -> Image.Image:
        """Find and load separate texture. Useful when multiple textue files needs to be loaded"""
        resolved_path = self.find_texture(path)
        logger.info("loading %s", resolved_path)
        if not resolved_path:
            raise ImproperlyConfigured("Cannot find texture: {}".format(path))

        image = Image.open(resolved_path)
        return self._apply_modifiers(image)

    def _apply_modifiers(self, image: Image.Image) -> Image.Image:
        if self.meta.flip_x:
            image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        if self.meta.flip_y:
            image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

        return self._palette_to_raw(image)

    def _palette_to_raw(self, image: Image.Image, mode: Optional[str] = None) -> Image.Image:
        """Converts image to raw if palette is present"""
        if image.palette and image.palette.mode.lower() in ["rgb", "rgba"]:
            mode = mode or image.palette.mode
            logger.debug("Converting P image to %s using palette", mode)
            return image.convert(mode)

        return image

    def _close_image(self) -> None:
        self.image.close()


def image_data(image: Image.Image) -> tuple[int, bytes]:
    """Get components and bytes for an image.
    The number of components is assumed by image
    size and the byte length of the raw data.

    Returns:
        tuple[int, bytes]: Number of components, byte data
    """
    # NOTE: We might want to check the actual image.mode
    #       and convert to an acceptable format.
    #       At the moment we load the data as is.
    data = image.tobytes()
    components = len(data) // (image.size[0] * image.size[1])
    logger.debug(
        "image_data size=[%s, %s] components=%s bytes=%s",
        image.size[0],
        image.size[1],
        components,
        len(data),
    )
    return components, data
