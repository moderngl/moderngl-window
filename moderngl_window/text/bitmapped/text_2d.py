from pathlib import Path
from typing import Optional

import glm
import moderngl
import numpy

from moderngl_window import resources
from moderngl_window.meta import DataDescription, ProgramDescription, TextureDescription
from moderngl_window.opengl.vao import VAO

from .base import BaseText, FontMeta

resources.register_dir(Path(__file__).parent.resolve())


class TextWriter2D(BaseText):
    """Simple monospaced bitmapped text renderer"""

    def __init__(self) -> None:
        super().__init__()

        meta = FontMeta(resources.data.load(DataDescription(path="bitmapped/text/meta.json")))
        self._texture = resources.textures.load(
            TextureDescription(
                path="bitmapped/textures/VeraMono.png",
                kind="array",
                mipmap=True,
                layers=meta.characters,
            )
        )
        self._program = resources.programs.load(
            ProgramDescription(path="bitmapped/programs/text_2d.glsl")
        )

        self._init(meta)

        assert self.ctx is not None, "There was a problem, we do not have a context"

        self._string_buffer = self.ctx.buffer(reserve=1024 * 4)
        self._string_buffer.clear(chunk=b"\32")
        pos = self.ctx.buffer(data=bytes([0] * 4 * 3))

        self._vao = VAO("textwriter", mode=moderngl.POINTS)
        self._vao.buffer(pos, "3f", "in_position")
        self._vao.buffer(self._string_buffer, "1u/i", "in_char_id")

        self._text: Optional[str] = None

    @property
    def text(self) -> Optional[str]:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value
        self._string_buffer.orphan(size=len(value) * 4)
        self._string_buffer.clear(chunk=b"\32")
        self._write(value)

    def _write(self, text: str) -> None:
        self._string_buffer.clear(chunk=b"\32")

        self._string_buffer.write(
            numpy.fromiter(
                self._translate_string(text),
                dtype=numpy.uint32,
            )
        )

    def draw(self, pos: tuple[float, float], length: int = -1, size: float = 24.0) -> None:
        assert self.ctx is not None, "There was a problem, we do not have a context"
        assert self.ctx.fbo is not None, "The current context do not have a framebuffer"
        assert self._meta is not None, "We are missing the information needed to write text"

        # Calculate ortho projection based on viewport
        vp = self.ctx.fbo.viewport
        w, h = vp[2], vp[3]
        projection = glm.ortho(
            0,  # left
            w,  # right
            0,  # bottom
            h,  # top
            1.0,  # near
            -1.0,  # far
        )

        self._texture.use(location=0)
        self._program["m_proj"].write(projection)
        self._program["text_pos"].value = pos
        self._program["font_texture"].value = 0
        self._program["char_size"].value = self._meta.char_aspect_wh * size, size

        self._vao.render(self._program, instances=len(self._text if self._text is not None else ""))
