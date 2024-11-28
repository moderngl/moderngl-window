from pathlib import Path
from unittest import TestCase

from utils import settings_context

from moderngl_window import resources
from moderngl_window.conf import settings
from moderngl_window.exceptions import ImproperlyConfigured


class ResourcesTestCase(TestCase):
    relative_path = './resources'
    absolute_path = (Path(__file__).parent.resolve() / Path('fixtures/resources'))
    nonexist_path = (Path(__file__).parent.resolve() / 'resources')
    file_path = Path(__file__).resolve()

    settings = {
        'DATA_DIRS': [],
        'PROGRAM_DIRS': [],
        'TEXTURE_DIRS': [],
        'SCENE_DIRS': [],
    }

    def test_register_program_dir(self):
        """Register a program dir"""
        with settings_context(self.settings):
            resources.register_program_dir(self.absolute_path)
            self.assertEqual(len(settings.PROGRAM_DIRS), 1)

    def test_register_texture_dir(self):
        """Register a texture dir"""
        with settings_context(self.settings):
            resources.register_texture_dir(self.absolute_path)
            self.assertEqual(len(settings.TEXTURE_DIRS), 1)

    def test_register_scene_dir(self):
        """Register a scene dir"""
        with settings_context(self.settings):
            resources.register_scene_dir(self.absolute_path)
            self.assertEqual(len(settings.SCENE_DIRS), 1)

    def test_register_data_dir(self):
        """Register a data dir"""
        with settings_context(self.settings):
            resources.register_data_dir(self.absolute_path)
            self.assertEqual(len(settings.DATA_DIRS), 1)

    def test_relative_path(self):
        """Raise error if relative path is passed"""
        with settings_context(self.settings):
            with self.assertRaises(ImproperlyConfigured):
                resources.register_dir(self.relative_path)

    def test_non_dir(self):
        """Register nonexistent path"""
        with settings_context(self.settings):
            with self.assertRaises(ImproperlyConfigured):
                resources.register_dir(self.nonexist_path)

    def test_register_file(self):
        """Attempt to register a file as a search path"""
        with settings_context(self.settings):
            with self.assertRaises(ImproperlyConfigured):
                resources.register_dir(self.file_path)

    def test_reister_path_duplicates(self):
        """Ensure search path only occur once if registered multipel times"""
        with settings_context(self.settings):
            resources.register_dir(self.absolute_path)
            resources.register_dir(self.absolute_path)
            resources.register_dir(self.absolute_path)
            self.assertEqual(len(settings.DATA_DIRS), 1)
