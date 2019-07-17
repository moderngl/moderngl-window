from headless import HeadlessTestCase

from moderngl_window.geometry import AttributeNames


class GeomtryTestCase(HeadlessTestCase):

    def test_attributes(self):
        attrs = AttributeNames(
            position="vertex",
            normal="normals",
        )
        self.assertEqual(attrs.POSITION, "vertex")
        self.assertEqual(attrs.NORMAL, "normals")
        self.assertEqual(attrs.TANGENT, "in_tangent")
