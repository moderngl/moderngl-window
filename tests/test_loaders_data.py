from pathlib import Path
from unittest import TestCase

from moderngl_window import resources
from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.meta import DataDescription

resources.register_dir((Path(__file__).parent / 'fixtures' / 'resources').resolve())


class DataLoaderTestcase(TestCase):

    def test_txt(self):
        """Ensure correct loader is selected by looking at file extension (txt)"""
        text = resources.data.load(DataDescription(path='data/data.txt'))
        self.assertEqual(text, "Hello")

    def test_json(self):
        """Ensure correct loader is selected by looking at file extension (json)"""
        json = resources.data.load(DataDescription(path='data/data.json'))
        self.assertEqual(json, {"test": "Hello"})

    def test_binary_kind(self):
        """Loading a binary file"""
        data = resources.data.load(DataDescription(path='data/data.bin', kind="binary"))
        self.assertEqual(data, b'Hello')

    def test_text_kind(self):
        """Load a e textfile"""
        text = resources.data.load(DataDescription(path='data/data.txt', kind="text"))
        self.assertEqual(text, "Hello")

    def test_json_kind(self):
        """Load a json file"""
        json = resources.data.load(DataDescription(path='data/data.json', kind="json"))
        self.assertEqual(json, {"test": "Hello"})

    def test_txt_not_found(self):
        """Ensure ImproperlyConfigured is raised if file is not found"""
        with self.assertRaises(ImproperlyConfigured):
            resources.data.load(DataDescription(path='data/notfound.txt'))

    def test_json_not_found(self):
        """Ensure ImproperlyConfigured is raised if file is not found"""
        with self.assertRaises(ImproperlyConfigured):
            resources.data.load(DataDescription(path='data/notfound.json'))

    def test_binary_not_found(self):
        """Ensure ImproperlyConfigured is raised if file is not found"""
        with self.assertRaises(ImproperlyConfigured):
            resources.data.load(DataDescription(path='data/notfound.bin', kind="binary"))

    def test_binary_abspath(self):
        """Strip search directories and use absolute path"""
        path = (Path(__file__).parent / "fixtures/resources/data/data.json").resolve()
        with resources.temporary_dirs([]):
            json = resources.data.load(DataDescription(path=path, kind="json"))
            self.assertEqual(json, {"test": "Hello"})
