from unittest import TestCase

import glm

from moderngl_window.opengl.projection import Projection3D


class Projection3DTestCase(TestCase):

    def test_default(self):
        """Test default values"""
        proj = Projection3D()
        self.assertAlmostEqual(proj.aspect_ratio, 16 / 9)
        self.assertEqual(proj.fov, 75.0)
        self.assertEqual(proj.near, 1.0)
        self.assertEqual(proj.far, 100.0)
        self.assertIsInstance(proj.projection_constants, tuple)
        self.assertAlmostEqual(proj.projection_constants[0], 1.01, places=2)
        self.assertAlmostEqual(proj.projection_constants[1], -1.01, places=2)
        self.assertIsInstance(proj.matrix, glm.mat4)
        self.assertIsInstance(proj.tobytes(), bytes)

    def test_update(self):
        """Update properties"""
        proj = Projection3D()
        proj.update(aspect_ratio=1.0, fov=100.0, near=0.01, far=10.0)
        self.assertAlmostEqual(proj.aspect_ratio, 1.0)
        self.assertEqual(proj.fov, 100.0)
        self.assertEqual(proj.near, 0.01)
        self.assertEqual(proj.far, 10.0)
        self.assertIsInstance(proj.projection_constants, tuple)
