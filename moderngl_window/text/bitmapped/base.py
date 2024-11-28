from typing import Any, Generator, Optional, Union

import moderngl_window


class FontMeta:
    """Metdata for texture array"""

    def __init__(self, meta: dict[str, Union[int, list[dict[str, int]]]]):
        self._meta = meta

        assert isinstance(self._meta["characters"], int)
        assert isinstance(self._meta["character_height"], int)
        assert isinstance(self._meta["character_width"], int)
        assert isinstance(self._meta["atlas_height"], int)
        assert isinstance(self._meta["atlas_width"], int)
        assert isinstance(self._meta["character_ranges"], list)

        self.characters = self._meta["characters"]
        self.character_ranges = self._meta["character_ranges"]
        self.character_height = self._meta["character_height"]
        self.character_width = self._meta["character_width"]
        self.atlas_height = self._meta["atlas_height"]
        self.atlas_width = self._meta["atlas_width"]

    @property
    def char_aspect_wh(self) -> float:
        return self.character_width / self.character_height

    def char_aspect_hw(self) -> float:
        return self.character_height / self.character_width


class BaseText:
    """Simple base class for a bitmapped text rendered"""

    def __init__(self) -> None:
        self._meta: Optional[FontMeta] = None
        self._ct: list[int] = []
        self.ctx = moderngl_window.ContextRefs.CONTEXT

    def draw(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()

    def _translate_string(self, data: str) -> Generator[int, None, None]:
        """Translate string into character texture positions"""
        assert (self._meta is not None) and (
            self._ct is not None
        ), "_meta or _ct (or both) are empty. Did you call _init()?"
        data_bytes = data.encode("iso-8859-1", errors="replace")

        for index, char in enumerate(data_bytes):
            yield self._meta.characters - 1 - self._ct[char]

    def _init(self, meta: FontMeta) -> None:
        self._meta = meta
        # Check if the atlas size is sane
        if not self._meta.characters * self._meta.character_height == self._meta.atlas_height:
            raise ValueError("characters * character_width != atlas_height")

        self._generate_character_map()

    def _generate_character_map(self) -> None:
        """Generate character translation map (latin1 pos to texture pos)"""
        assert self._meta is not None, "You should not call _generate_character_map but _init"
        self._ct = [-1] * 256
        index = 0
        for c_range in self._meta.character_ranges:
            for c_pos in range(c_range["min"], c_range["max"] + 1):
                self._ct[c_pos] = index
                index += 1
