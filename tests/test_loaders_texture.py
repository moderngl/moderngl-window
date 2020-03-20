from pathlib import Path

import moderngl
from headless import HeadlessTestCase
from moderngl_window import resources
from moderngl_window.meta import TextureDescription
from moderngl_window.exceptions import ImproperlyConfigured

resources.register_dir((Path(__file__).parent / 'fixtures' / 'resources').resolve())


class TextureLoadersTestCase(HeadlessTestCase):
    window_size = (16, 16)
    aspect_ratio = 1.0

    def test_texture_2d(self):
        """Load standard 2d texture"""
        texture = resources.textures.load(TextureDescription(path='textures/crate.png'))
        self.assertEqual(texture.size, (192, 192))
        self.assertIsInstance(texture.extra.get('meta'), TextureDescription)

    def test_texture_2d_8bit(self):
        """Test loading 8 bit texture with palette"""
        texture = resources.textures.load(TextureDescription(path='textures/8bit.png'))
        self.assertIsInstance(texture, moderngl.Texture)

    def test_texture_not_found(self):
        """Ensure ImproperlyConfigured is raised if texture is not found"""
        with self.assertRaises(ImproperlyConfigured):
            resources.textures.load(TextureDescription(path='textures/doesnotexist.png'))

    def test_texture_array(self):
        """Load texture array"""
        texture = resources.textures.load(
            TextureDescription(path='textures/array.png', layers=10, kind="array")
        )
        self.assertEqual(texture.size, (256, 256, 10))
        self.assertIsInstance(texture.extra.get('meta'), TextureDescription)

    def test_texture_array_no_layers(self):
        """Ensure error is raised when no layer is defined"""
        with self.assertRaises(ImproperlyConfigured):
            resources.textures.load(
                TextureDescription(path='textures/array.png', kind="array")
            )

    def test_cubemap(self):
        texture = resources.textures.load(TextureDescription(
            pos_x='textures/cubemap/pos_x.png',
            pos_y='textures/cubemap/pos_y.png',
            pos_z='textures/cubemap/pos_z.png',
            neg_x='textures/cubemap/neg_z.png',
            neg_y='textures/cubemap/neg_y.png',
            neg_z='textures/cubemap/neg_z.png',
            kind='cube',
        ))
        self.assertIsInstance(texture, moderngl.TextureCube)

    def test_texture_mimpamps(self):
        """Load texture with mipmapping and anisotropy"""
        desc = TextureDescription(
            path='textures/crate.png',
            mipmap_levels=(0, 2),
            anisotropy=4.0,
        )
        texture = resources.textures.load(desc)
        self.assertEqual(texture.anisotropy, 4.0)
        self.assertEqual(desc.mipmap, True)

        # Texture Array
        desc = TextureDescription(
            path='textures/array.png',
            kind="array",
            layers=10,
            mipmap_levels=(0, 5),
            anisotropy=8.0,
        )
        texture = resources.textures.load(desc)
        self.assertEqual(texture.anisotropy, 8.0)
        self.assertEqual(desc.mipmap, True)
