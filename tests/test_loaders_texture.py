from pathlib import Path

from headless import HeadlessTestCase
from moderngl_window import resources
from moderngl_window.meta import TextureDescription

resources.register_dir((Path(__file__).parent / 'fixtures' / 'resources').resolve())


class TextureLoadersTestCase(HeadlessTestCase):
    window_size = (16, 16)
    aspect_ratio = 1.0

    def test_texture_2d(self):
        texture = resources.textures.load(TextureDescription(path='textures/crate.png'))
        self.assertEqual(texture.size, (192, 192))

    def test_texture_array(self):
        texture = resources.textures.load(
            TextureDescription(path='textures/array.png', layers=10, kind="array")
        )
        self.assertEqual(texture.size, (256, 256, 10))
