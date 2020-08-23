import logging
import os
from datetime import datetime
from typing import Union

import moderngl
from PIL import Image
from moderngl_window.conf import settings

logger = logging.getLogger(__name__)

TEXTURE_MODES = [None, "L", None, "RGB", "RGBA"]


def create(
    source: Union[moderngl.Framebuffer, moderngl.Texture],
    file_format="png",
    name: str = None,
    mode="RGB",
    alignment=1,
):
    """
    Create a screenshot from a ``moderngl.Framebuffer`` or ``moderngl.Texture``.
    The screenshot will be written to :py:attr:`~moderngl_window.conf.Settings.SCREENSHOT_PATH`
    if set or ``cwd`` or an absolute path can be used.

    Args:
        source: The framebuffer or texture to screenshot
        file_format (str): formats supported by PIL (png, jpeg etc)
        name (str): Optional file name with relative or absolute path
        mode (str): Components/mode to use
        alignment (int): Buffer alignment
    """
    dest = ""
    if settings.SCREENSHOT_PATH:
        if not os.path.exists(str(settings.SCREENSHOT_PATH)):
            logger.debug(
                "SCREENSHOT_PATH does not exist. creating: %s", settings.SCREENSHOT_PATH
            )
            os.makedirs(str(settings.SCREENSHOT_PATH))
        dest = settings.SCREENSHOT_PATH
    else:
        logger.info("SCREENSHOT_PATH not defined in settings. Using cwd as fallback.")

    if not name:
        name = "{}.{}".format(
            datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"), file_format
        )

    logger.debug(
        "Creating screenshot: source=%s file_format=%s name=%s mode=%s alignment=%s",
        source,
        file_format,
        name,
        mode,
        alignment,
    )

    if isinstance(source, moderngl.Framebuffer):
        image = Image.frombytes(
            mode,
            (
                source.viewport[2] - source.viewport[0],
                source.viewport[3] - source.viewport[1],
            ),
            source.read(viewport=source.viewport, alignment=alignment),
        )
    elif isinstance(source, moderngl.Texture):
        image = Image.frombytes(
            TEXTURE_MODES[source.components], source.size, source.read(alignment=1)
        )
    else:
        raise ValueError(
            "Source needs to be a FrameBuffer or Texture, not a %s", type(source)
        )

    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    dest = os.path.join(str(dest), name)
    logger.info("Creating screenshot: %s", dest)
    image.save(dest, format=file_format)
