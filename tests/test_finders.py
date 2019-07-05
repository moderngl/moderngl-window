from pathlib import Path
from unittest import TestCase

from moderngl_window.finders import (
    data,
    program,
    texture,
    scene,
)

from utils import settings, rnd_string


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
        with settings(self.finder_settings):
            finder = data.FileSystemFinder()
            result = finder.find('data.json')
            self.assertIsInstance(result, Path)
            self.assertTrue(result.name, 'data.json')

    def test_program_finder(self):
        """Find a glsl file"""
        with settings(self.finder_settings):
            finder = program.FileSystemFinder()
            result = finder.find('test.glsl')
            self.assertIsInstance(result, Path)
            self.assertTrue(result.name, 'test.glsl')

    def test_texture_finder(self):
        with settings(self.finder_settings):
            finder = texture.FileSystemFinder()
            result = finder.find('image.png')
            self.assertIsInstance(result, Path)
            self.assertTrue(result.name, 'image.png')

    def test_scene_finder(self):
        with settings(self.finder_settings):
            finder = scene.FileSystemFinder()
            result = finder.find('model.obj')
            self.assertIsInstance(result, Path)
            self.assertTrue(result.name, 'model.obj')
