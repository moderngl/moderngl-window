
import moderngl_window


class FontMeta:
    """Metdata for texture array"""

    def __init__(self, meta):
        self._meta = meta
        self.characters = self._meta['characters']
        self.character_ranges = self._meta['character_ranges']
        self.character_height = self._meta['character_height']
        self.character_width = self._meta['character_width']
        self.atlas_height = self._meta['atlas_height']
        self.atlas_width = self._meta['atlas_width']

    @property
    def char_aspect_wh(self):
        return self.character_width / self.character_height

    def char_aspect_hw(self):
        return self.character_height / self.character_width


class BaseText:
    """Simple base class for a bitmapped text rendered"""

    def __init__(self):
        self._meta = None
        self._ct = None
        self.ctx = moderngl_window.ContextRefs.CONTEXT

    def draw(self, *args, **kwargs):
        raise NotImplementedError()

    def _translate_string(self, data):
        """Translate string into character texture positions"""
        data = data.encode('iso-8859-1', errors='replace')

        for index, char in enumerate(data):
            yield self._meta.characters - 1 - self._ct[char]

    def _init(self, meta: FontMeta):
        self._meta = meta
        # Check if the atlas size is sane
        if not self._meta.characters * self._meta.character_height == self._meta.atlas_height:
            raise ValueError("characters * character_width != atlas_height")

        self._generate_character_map()

    def _generate_character_map(self):
        """Generate character translation map (latin1 pos to texture pos)"""
        self._ct = [-1] * 256
        index = 0
        for c_range in self._meta.character_ranges:
            for c_pos in range(c_range['min'], c_range['max'] + 1):
                self._ct[c_pos] = index
                index += 1
