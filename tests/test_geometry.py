from headless import HeadlessTestCase

from moderngl_window import geometry
from moderngl_window.geometry import AttributeNames
from moderngl_window.opengl.vao import BufferInfo


class GeomtryTestCase(HeadlessTestCase):
    custom_attrs = AttributeNames(
        position="test_pos",
        normal="test_normal",
        texcoord_0="test_uv0",
    )

    def test_bbox(self):
        """Create a bounding box"""
        mesh = geometry.bbox(size=(1.0, 1.0, 1.0), name="test_bbox")
        self.assertEqual(mesh.name, "test_bbox")
        self.assertIsInstance(mesh.get_buffer_by_name(AttributeNames.POSITION), BufferInfo)

        # Use custom buffer/attribute names
        mesh = geometry.bbox(size=(1.0, 1.0, 1.0), name="test_bbox", attr_names=self.custom_attrs)
        self.assertIsInstance(mesh.get_buffer_by_name(self.custom_attrs.POSITION), BufferInfo)

    def test_cube(self):
        """Create a cube"""
        mesh = geometry.cube(size=(1.0, 1.0, 1.0), name="test_cube")
        self.assertEqual(mesh.name, "test_cube")
        self.assertIsInstance(mesh.get_buffer_by_name(AttributeNames.POSITION), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name(AttributeNames.NORMAL), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name(AttributeNames.TEXCOORD_0), BufferInfo)

        # Use custom buffer/attribute names
        mesh = geometry.cube(size=(1.0, 1.0, 1.0), name="test_cube", attr_names=self.custom_attrs)
        self.assertIsInstance(mesh.get_buffer_by_name(self.custom_attrs.POSITION), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name(self.custom_attrs.NORMAL), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name(self.custom_attrs.TEXCOORD_0), BufferInfo)

    def test_quad_fs(self):
        """Create a fullscreen quad"""
        mesh = geometry.quad_fs(name="test_quad_fs")
        self.assertEqual(mesh.name, "test_quad_fs")
        self.assertIsInstance(mesh.get_buffer_by_name(AttributeNames.POSITION), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name(AttributeNames.NORMAL), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name(AttributeNames.TEXCOORD_0), BufferInfo)

        # Use custom buffer/attribute names
        mesh = geometry.quad_fs(name="test_quad_fs", attr_names=self.custom_attrs)
        self.assertIsInstance(mesh.get_buffer_by_name(self.custom_attrs.POSITION), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name(self.custom_attrs.NORMAL), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name(self.custom_attrs.TEXCOORD_0), BufferInfo)

    def test_sphere(self):
        """Create a spwhere"""
        mesh = geometry.sphere(radius=2.0, sectors=32, rings=16, name="test_sphere")
        self.assertEqual(mesh.name, "test_sphere")
        self.assertIsInstance(mesh.get_buffer_by_name(AttributeNames.POSITION), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name(AttributeNames.NORMAL), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name(AttributeNames.TEXCOORD_0), BufferInfo)

        # Use custom buffer/attribute names
        mesh = geometry.sphere(radius=2.0, sectors=32, rings=16, name="test_sphere", attr_names=self.custom_attrs)
        self.assertIsInstance(mesh.get_buffer_by_name(self.custom_attrs.POSITION), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name(self.custom_attrs.NORMAL), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name(self.custom_attrs.TEXCOORD_0), BufferInfo)
