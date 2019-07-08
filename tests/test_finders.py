from pathlib import Path
from unittest import TestCase

from moderngl_window.finders import (
    data,
    program,
    texture,
    scene,
)
from moderngl_window.exceptions import ImproperlyConfigured

from utils import settings_context


class FinderTestCase(TestCase):
    root = Path(__file__).parent / 'fixtures' / 'resources'
    finder_settings = {
        'DATA_DIRS': [Path(root, 'data')],
        'PROGRAM_DIRS': [Path(root, 'programs')],
        'TEXTURE_DIRS': [Path(root, 'textures')],
        'SCENE_DIRS': [Path(root, 'scenes')],
    }

    def test_data_finder(self):
        """Find a data file"""
        with settings_context(self.finder_settings):
            result = data.FileSystemFinder().find('data.json')
            self.assertIsInstance(result, Path)
            self.assertTrue(result.name, 'data.json')

    def test_program_finder(self):
        """Find a glsl file"""
        with settings_context(self.finder_settings):
            result = program.FileSystemFinder().find('test.glsl')
            self.assertIsInstance(result, Path)
            self.assertTrue(result.name, 'test.glsl')

    def test_texture_finder(self):
        """Find a texture"""
        with settings_context(self.finder_settings):
            result = texture.FileSystemFinder().find('image.png')
            self.assertIsInstance(result, Path)
            self.assertTrue(result.name, 'image.png')

    def test_scene_finder(self):
        """Find a scene"""
        with settings_context(self.finder_settings):
            result = scene.FileSystemFinder().find('model.obj')
            self.assertIsInstance(result, Path)
            self.assertTrue(result.name, 'model.obj')

    def test_relative_path_raises_exception(self):
        with settings_context({'DATA_DIRS': ['relative_location']}):
            with self.assertRaises(ImproperlyConfigured):
                data.FileSystemFinder().find('something')
