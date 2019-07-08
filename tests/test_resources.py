from unittest import TestCase
from pathlib import Path

from moderngl_window import resources
from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.conf import settings

from utils import settings_context


class ResourcesTestCase(TestCase):
    relative_path = './resources'
    absolute_path = (Path(__file__).parent / 'resources').resolve()
    settings = {
        'DATA_DIRS': [],
        'PROGRAM_DIRS': [],
        'TEXTURE_DIRS': [],
        'SCENE_DIRS': [],
    }

    def test_relative_path(self):
        """Raise error if relative path is passed"""
        with self.assertRaises(ImproperlyConfigured):
            print(self.relative_path)
            resources.register_dir(self.relative_path)

    def test_register_program_dir(self):
        with settings_context(self.settings):
            resources.register_program_dir(self.absolute_path)
            self.assertEqual(len(settings.PROGRAM_DIRS), 1)

    def test_register_texture_dir(self):
        with settings_context(self.settings):
            resources.register_texture_dir(self.absolute_path)
            self.assertEqual(len(settings.TEXTURE_DIRS), 1)

    def test_register_scene_dir(self):
        with settings_context(self.settings):
            resources.register_scene_dir(self.absolute_path)
            self.assertEqual(len(settings.SCENE_DIRS), 1)

    def test_register_data_dir(self):
        with settings_context(self.settings):
            resources.register_data_dir(self.absolute_path)
            self.assertEqual(len(settings.DATA_DIRS), 1)
