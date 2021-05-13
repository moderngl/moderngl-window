import numpy
from pyrr import matrix44

from pathlib import Path

import moderngl
from moderngl_window.opengl.vao import VAO
from moderngl_window import resources
from moderngl_window.meta import (
    DataDescription,
    TextureDescription,
    ProgramDescription,
)

from .base import BaseText, FontMeta

resources.register_dir(Path(__file__).parent.resolve())


class TextWriter2D(BaseText):
    """Simple monspaced bitmapped text renderer"""

    def __init__(self):
        super().__init__()

        meta = FontMeta(resources.data.load(
            DataDescription(path="bitmapped/text/meta.json")
        ))
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

        self._string_buffer = self.ctx.buffer(reserve=1024 * 4)
        self._string_buffer.clear(chunk=b'\32')
        pos = self.ctx.buffer(data=bytes([0] * 4 * 3))

        self._vao = VAO("textwriter", mode=moderngl.POINTS)
        self._vao.buffer(pos, '3f', 'in_position')
        self._vao.buffer(self._string_buffer, '1u/i', 'in_char_id')

        self._text: str = None

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        print(len(value))
        self._text = value
        self._string_buffer.orphan(size=len(value) * 4)
        self._string_buffer.clear(chunk=b'\32')
        self._write(value)

    def _write(self, text: str):
        self._string_buffer.clear(chunk=b'\32')

        print(self._string_buffer.size)
        self._string_buffer.write(
            numpy.fromiter(
                self._translate_string(text),
                dtype=numpy.uint32,
            )
        )

    def draw(self, pos, length=-1, size=24.0):
        # Calculate ortho projection based on viewport
        vp = self.ctx.fbo.viewport
        w, h = vp[2] - vp[0], vp[3] - vp[1]
        projection = matrix44.create_orthogonal_projection_matrix(
            0,  # left
            w,  # right
            0,  # bottom
            h,  # top
            1.0,  # near
            -1.0,  # far
            dtype=numpy.float32,
        )

        self._texture.use(location=0)
        self._program["m_proj"].write(projection)
        self._program["text_pos"].value = pos
        self._program["font_texture"].value = 0
        self._program["char_size"].value = self._meta.char_aspect_wh * size, size

        self._vao.render(self._program, instances=len(self._text))
