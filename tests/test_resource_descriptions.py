from unittest import TestCase

from moderngl_window.meta import (
    DataDescription,
    ProgramDescription,
    SceneDescription,
    TextureDescription,
)
from moderngl_window.resources.base import ResourceDescription


class ResourceDescriptionTestCase(TestCase):
    path = 'path/to'
    label = 'label'
    kind = 'somekind'

    def test_base(self):
        """Create a base resource description"""
        instance = ResourceDescription(
            path=self.path,
            label=self.label,
            kind=self.kind,
        )
        self.inspect_base_properties(instance)
        str(instance)
        repr(instance)

    def inspect_base_properties(self, instance):
        self.assertEqual(instance.path, self.path)
        self.assertEqual(instance.label, self.label)
        self.assertEqual(instance.kind, self.kind)
        self.assertEqual(instance.loader_cls, None)
        self.assertEqual(instance.resolved_path, None)
        self.assertIsInstance(instance.attrs, dict)

        instance.kind = 'otherkind'
        instance.loader_cls = 'fake_loader_cls'
        self.assertEqual(instance.kind, 'otherkind')
        self.assertEqual(instance.loader_cls, 'fake_loader_cls')

    def test_data(self):
        """Create a DataDescription"""
        instance = DataDescription(
            path=self.path,
            kind=self.kind,
            label=self.label,
        )
        self.inspect_base_properties(instance)

    def test_program(self):
        """Create ProgramDescription"""
        instance = ProgramDescription(
            path=self.path,
            kind=self.kind,
            label=self.label,
            vertex_shader='vertex_shader',
            geometry_shader='geometry_shader',
            fragment_shader='fragment_shader',
            tess_control_shader='tess_control_shader',
            tess_evaluation_shader='tess_evaluation_shader',
        )
        self.inspect_base_properties(instance)
        self.assertEqual(instance.reloadable, False)
        self.assertEqual(instance.vertex_shader, 'vertex_shader')
        self.assertEqual(instance.geometry_shader, 'geometry_shader')
        self.assertEqual(instance.fragment_shader, 'fragment_shader')
        self.assertEqual(instance.tess_control_shader, 'tess_control_shader')
        self.assertEqual(instance.tess_evaluation_shader, 'tess_evaluation_shader')

    def test_scene(self):
        """Create SceneDescription"""
        instance = SceneDescription(
            path=self.path,
            kind=self.kind,
            label=self.label,
        )
        self.assertFalse(instance.cache)
        self.inspect_base_properties(instance)

    def test_texture(self):
        """Create TextureDescription"""
        instance = TextureDescription(
            path=self.path,
            kind=self.kind,
            label=self.label,
        )
        self.inspect_base_properties(instance)
        self.assertEqual(instance.flip_x, False)
        self.assertEqual(instance.flip_y, True)
        self.assertEqual(instance.mipmap, False)
        self.assertEqual(instance.mipmap_levels, None)
        self.assertEqual(instance.anisotropy, 1.0)
