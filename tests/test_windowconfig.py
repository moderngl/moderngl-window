from pathlib import Path

import moderngl
from headless import WindowConfigTestCase

from moderngl_window import WindowConfig
from moderngl_window.scene import Scene


class WindowConfigTestCase(WindowConfigTestCase):
    class TestConfig(WindowConfig):
        window_size = (16, 32)
        aspect_ratio = 1.0
        gl_version = (4, 1)
        title = "Test"
        resource_dir = Path(__file__).parent / 'fixtures' / 'resources'

    def create_window_config(self, cls):
        """Create a WindowConfig instance passing in the standard params"""
        instance = cls(ctx=self.window.ctx, wnd=self.window, timer=None)
        instance.window_size = self.config.window_size
        instance.aspect_ratio = self.config.aspect_ratio
        instance.gl_version = self.config.gl_version
        return instance

    def test_properties(self):
        """Ensure all callback funcs are callable"""
        # Configured Values
        self.assertIsInstance(self.window.config, WindowConfig)
        self.assertEqual(self.window.size, self.config.window_size)
        self.assertEqual(self.window.width, self.config.window_size[0])
        self.assertEqual(self.window.height, self.config.window_size[1])
        self.assertEqual(self.window.title, self.config.title)
        self.assertEqual(self.window.gl_version, self.config.gl_version)
        self.assertEqual(self.config.aspect_ratio, self.window.aspect_ratio)
        self.assertIsInstance(self.window.ctx, moderngl.Context)
        self.assertIsInstance(self.window.fbo, moderngl.Framebuffer)
        self.assertEqual(self.window.vsync, False)

        # Defaults
        self.assertEqual(self.config.resizable, True)  # Disabled in headless
        self.assertEqual(self.config.cursor, True)  # Disabled in headless
        self.assertEqual(self.config.samples, self.window.samples)
        self.assertIsInstance(self.config.resource_dir, Path)
        self.assertEqual(self.config.clear_color, (0, 0, 0, 0))

        # Ensure callback funcs are actual callable
        self.assertTrue(callable(self.window.resize_func))
        self.assertTrue(callable(self.window.key_event_func))
        self.assertTrue(callable(self.window.mouse_position_event_func))
        self.assertTrue(callable(self.window.mouse_press_event_func))
        self.assertTrue(callable(self.window.mouse_release_event_func))
        self.assertTrue(callable(self.window.mouse_drag_event_func))
        self.assertEqual(self.window.pixel_ratio, 1.0)
        self.assertEqual(self.window.buffer_size, self.config.window_size)
        self.assertEqual(self.window.buffer_width, self.config.window_size[0])
        self.assertEqual(self.window.buffer_height, self.config.window_size[1])

        # Other windows properties
        self.assertEqual(self.window.viewport, (0, 8, 16, 16))
        self.assertEqual(self.window.viewport_size, (16, 16))
        self.assertEqual(self.window.viewport_width, 16)
        self.assertEqual(self.window.viewport_height, 16)
        self.assertEqual(self.window.frames, 0)

        # set properties
        self.window.title = "Modified Title"
        self.assertEqual(self.window.title, "Modified Title")
        value = not self.window.cursor
        self.window.cursor = value
        self.assertEqual(self.window.cursor, value)
        value = self.window.position[0] + 10, self.window.position[1] + 10
        self.window.position = value
        self.assertEqual(self.window.position, value)

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
        """Load texture with shortcut method"""
        texture = self.config.load_texture_2d(
            "textures/crate.png",
            flip=True,
            mipmap_levels=(0, 2),
            anisotropy=4.0,
        )
        self.assertIsInstance(texture, moderngl.Texture)
        self.assertEqual(texture.anisotropy, 4.0)

    def test_load_texture_array(self):
        """Load texture array with shortcut method"""
        texture = self.config.load_texture_array(
            'textures/array.png',
            layers=10,
            flip=True,
            mipmap=False,
            mipmap_levels=(0, 2),
            anisotropy=4.0,
        )
        self.assertIsInstance(texture, moderngl.TextureArray)
        self.assertEqual(texture.anisotropy, 4.0)
        self.assertEqual(texture.layers, 10)

    def test_load_program_single(self):
        """Load a single glsl program"""
        prog = self.config.load_program(path='programs/white.glsl')
        self.assertIsInstance(prog, moderngl.Program)

    def test_load_program_multiple(self):
        """Load program from multiple shader files"""
        prog = self.config.load_program(
            vertex_shader='programs/terrain/terrain_vs.glsl',
            fragment_shader='programs/terrain/terrain_fs.glsl',
            tess_control_shader='programs/terrain/terrain_tc.glsl',
            tess_evaluation_shader='programs/terrain/terrain_te.glsl',
        )
        self.assertIsInstance(prog, moderngl.Program)

    def test_load_text(self):
        """Load text file"""
        text = self.config.load_text('data/data.txt')
        self.assertEqual(text, "Hello")

    def test_load_json(self):
        """Load a json file"""
        json = self.config.load_json('data/data.json')
        self.assertEqual(json, {"test": "Hello"})

    def test_load_binary(self):
        """Load binary file"""
        data = self.config.load_binary('data/data.bin')
        self.assertEqual(data, b'Hello')

    def test_load_scene(self):
        """Load a scene"""
        scene = self.config.load_scene(
            path='scenes/BoxTextured/glTF/BoxTextured.gltf',
            cache=False,
            attr_names=None,
            kind=None,
        )
        self.assertIsInstance(scene, Scene)
