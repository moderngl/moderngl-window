from unittest import TestCase

from moderngl_window.utils.module_loading import import_string


class UtilsTestCase(TestCase):

    def test_import_string(self):
        """Ensure importing a class returns a type"""
        cls = import_string('moderngl_window.context.headless.Window')
        self.assertEqual(type(cls), type)

    def test_import_error(self):
        """ImportError should be raised"""
        with self.assertRaises(ImportError):
            import_string('this.is.bs')

    def test_no_dotted_path(self):
        with self.assertRaises(ImportError):
            import_string('nonexistingmodule')

    def test_import_error_missing_cls(self):
        """ImportError when missin class in module"""
        with self.assertRaises(ImportError):
            import_string('moderngl_window.context.headless.NadaWindow')
