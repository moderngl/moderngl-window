from unittest import TestCase

from moderngl_window.finders import (
    data,
    program,
    textures,
    scenes,
)

from utils import settings


class FinderTestCase(TestCase):

    def test_data_finder(self):
        with settings({'DATA_DIRS': []}) as s:
            finder = data.FileSystemFinder()
            self.assertEqual(finder.find('something'), None)

    def test_program_finder(self):
        with settings({'PROGRAM_DIRS': []}) as s:
            finder = data.FileSystemFinder()
            self.assertEqual(finder.find('something'), None)

    def test_texture_finder(self):
        with settings({'TEXTURE_DIRS': []}) as s:
            finder = data.FileSystemFinder()
            self.assertEqual(finder.find('something'), None)

    def test_scene_finder(self):
        with settings({'SCENE_DIRS': []}) as s:
            finder = data.FileSystemFinder()
            self.assertEqual(finder.find('something'), None)
