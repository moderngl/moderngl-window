from pathlib import Path
from unittest import TestCase

from utils import settings_context

from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.finders import data, program, scene, texture
from moderngl_window.finders.base import BaseFilesystemFinder


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
            result = data.FilesystemFinder().find(Path('data.json'))
            self.assertIsInstance(result, Path)
            self.assertTrue(result.name, 'data.json')

    def test_program_finder(self):
        """Find a glsl file"""
        with settings_context(self.finder_settings):
            result = program.FilesystemFinder().find(Path('test.glsl'))
            self.assertIsInstance(result, Path)
            self.assertTrue(result.name, 'test.glsl')

    def test_texture_finder(self):
        """Find a texture"""
        with settings_context(self.finder_settings):
            result = texture.FilesystemFinder().find(Path('image.png'))
            self.assertIsInstance(result, Path)
            self.assertTrue(result.name, 'image.png')

    def test_scene_finder(self):
        """Find a scene"""
        with settings_context(self.finder_settings):
            result = scene.FilesystemFinder().find(Path('model.obj'))
            self.assertIsInstance(result, Path)
            self.assertTrue(result.name, 'model.obj')

    def test_relative_path_raises_exception(self):
        with settings_context({'DATA_DIRS': ['relative_location']}):
            with self.assertRaises(ImproperlyConfigured):
                data.FilesystemFinder().find(Path('something'))

    def test_absolute_path(self):
        """Ensure absolute paths are ignored"""
        with settings_context(self.finder_settings):
            finder = data.FilesystemFinder()
            result = finder.find(Path(self.root, Path('data/data.json')))
            self.assertIsNone(result)

    def test_not_found(self):
        """Ensure finder returns non when nothing was found"""
        finder = data.FilesystemFinder()
        result = finder.find(Path(self.root, Path('data/idontexist.json')))
        self.assertIsNone(result)

    def test_no_search_dirs(self):
        """When no search dirs the finder should return None"""
        with settings_context({'DATA_DIRS': []}):
            finder = data.FilesystemFinder()
            result = finder.find(Path('data/data.json'))
            self.assertIsNone(result)

    def test_non_path(self):
        """Raise ValueError if finder gets non-Path instance"""
        finder = data.FilesystemFinder()
        with self.assertRaises(ValueError):
            finder.find('test')

    def test_custom_finder_missing_setting(self):
        """Ensure broken finder with nonexisting settings attr is detected"""
        class BrokenFinder(BaseFilesystemFinder):
            settings_attr = "NOPE"

        with self.assertRaises(ImproperlyConfigured):
            BrokenFinder()
