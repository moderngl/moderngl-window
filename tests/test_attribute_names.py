from unittest import TestCase

from moderngl_window.geometry import AttributeNames


class AttributeNamesTestCase(TestCase):

    def test_attributes(self):
        """Ensure we can create an instance with partial overrides"""
        attrs = AttributeNames(
            position="vertex",
            normal="normals",
        )
        self.assertEqual(attrs.POSITION, "vertex")
        self.assertEqual(attrs.NORMAL, "normals")
        self.assertEqual(attrs.TANGENT, "in_tangent")
