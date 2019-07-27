from pathlib import Path

import moderngl
from headless import WindowConfigTestCase
from moderngl_window import WindowConfig


class WindowConfigTestCase(WindowConfigTestCase):
    class TestConfig(WindowConfig):
        window_size = (16, 16)
        aspect_ratio = 1.0
        gl_version = (4, 1)
        title = "Test"
        resource_dir = Path(__file__).parent / 'fixtures' / 'resources'

    def create_window_config(self, cls):
        """Create a WindoeConfig instance passing in the standard params"""
        instance = cls(ctx=self.window.ctx, wnd=self.window, timer=None)
        instance.window_size = self.config.window_size
        instance.aspect_ratio = self.config.aspect_ratio
        instance.gl_version = self.config.gl_version
        return instance

    def test_properties(self):
        """Ensure all callback funcs are callable"""
        # Configured Values
        self.assertEqual(self.window.size, self.config.window_size)
        self.assertEqual(self.window.title, self.config.title)
        self.assertEqual(self.window.gl_version, self.config.gl_version)
        self.assertEqual(self.config.aspect_ratio, self.window.aspect_ratio)

        # Defaults
        self.assertEqual(self.config.resizable, True)  # Disabled in headless
        self.assertEqual(self.config.cursor, True)  # Disabled in headless
        self.assertEqual(self.config.samples, self.window.samples)
        self.assertIsInstance(self.config.resource_dir, Path)

        # Ensure callback funcs are actuall callable
        self.assertTrue(callable(self.window.resize_func))
        self.assertTrue(callable(self.window.key_event_func))
        self.assertTrue(callable(self.window.mouse_position_event_func))
        self.assertTrue(callable(self.window.mouse_press_event_func))
        self.assertTrue(callable(self.window.mouse_release_event_func))

    def test_missing_wnd_ctx(self):
        """Attempt creating WindogConfig without a window or ctx"""
        class TestConfig(WindowConfig):
            pass

        with self.assertRaises(ValueError):
            TestConfig(ctx=self.window.ctx)

        with self.assertRaises(ValueError):
            TestConfig(wnd=self.window)

    def test_set_bad_callback(self):
        """Attempt setting bad callbacks"""
        class TextConfig(WindowConfig):
            pass

        with self.assertRaises(ValueError):
            self.window.resize_func = None

        with self.assertRaises(ValueError):
            self.window.resize_func = "Hello"

    def test_load_texture_2d(self):
        """Load texure with shortcut method"""
        texture = self.config.load_texture_2d("textures/crate.png")
        self.assertIsInstance(texture, moderngl.Texture)

    def test_load_texture_array(self):
        """Load texture array with shortcut method"""
        texture = self.config.load_texture_array('textures/array.png', 10)
        self.assertIsInstance(texture, moderngl.TextureArray)
        self.assertEqual(texture.layers, 10)


