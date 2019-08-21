"""
Documentation testing
Inspired by:
https://github.com/cprogrammer1994/ModernGL/blob/master/tests/test_documentation.py
by Szabolcs Dombi
This version is simplified:
* Only test if the attribute or method is present in the class. Function parameters are not inspected.
* Include ignore pattern in the implemented set
"""
import os
import re
import types
import unittest

from moderngl_window.utils import module_loading


class TestCase(unittest.TestCase):
    """
    Test reference docs
    """
    def validate(self, filename, module, classname=None, ignore=None):
        """
        Finds all automethod and autoattribute statements in an rst file
        comparing them to the attributes found in the actual class
        """
        if ignore is None:
            ignore = []

        with open(os.path.normpath(os.path.join('docs', 'reference', filename))) as f:
            docs = f.read()

        module = module_loading.import_module(module)

        # Inspect class
        if classname:
            methods = re.findall(r'^\.\. automethod:: ([^\(\n]+)', docs, flags=re.M)
            attributes = re.findall(r'^\.\. autoattribute:: ([^\n]+)', docs, flags=re.M)

            documented = set(filter(lambda x: x.startswith(classname), [a for a in methods] + attributes))
            implemented = set(classname + '.' + x for x in dir(getattr(module, classname))
                              if not x.startswith('_') or x == '__init__')
            print(implemented)
            ignored = set(classname + '.' + x for x in ignore)
        # Inspect module
        else:
            # Only inspect functions for now
            functions = re.findall(r'^\.\. autofunction:: ([^\(\n]+)', docs, flags=re.M)
            documented = set(functions)
            ignored = set(ignore)
            implemented = set(func for func in dir(module) if isinstance(getattr(module, func), types.FunctionType))

        self.assertSetEqual(implemented - documented - ignored, set(), msg='Implemented but not Documented')
        self.assertSetEqual(documented - implemented - ignored, set(), msg='Documented but not Implemented')

    def test_moderngl_window(self):
        self.validate(
            'moderngl_window.rst',
            'moderngl_window',
            ignore=['valid_window_size', 'valid_window_size_multiplier', 'import_string', 'valid_bool'],
        )

    def test_settings(self):
        self.validate('settings.conf.settings.rst', 'moderngl_window.conf', 'Settings', [])

    def test_context_base_window(self):
        self.validate('context/basewindow.rst', 'moderngl_window.context.base.window', 'BaseWindow')

    def test_context_glfw_window(self):
        self.validate('context/glfw.window.rst', 'moderngl_window.context.glfw.window', 'Window')
