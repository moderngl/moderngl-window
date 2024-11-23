from unittest import TestCase
import numpy as np
import glm

from moderngl_window.scene import Camera, KeyboardCamera
from moderngl_window.scene import camera as cam
from moderngl_window.opengl.projection import Projection3D
from moderngl_window.context.base.keys import BaseKeys, KeyModifiers


class CameraTest(TestCase):
    """Simple camera testing"""

    def test_camera(self):
        camera = Camera(fov=60, aspect_ratio=1.0, near=1.0, far=100.0)
        self.assertIsInstance(camera.projection, Projection3D)
        self.assertIsInstance(camera.matrix, glm.mat4)

        camera.look_at(vec=glm.vec3(1, 2, 3))
        camera.look_at(pos=(4, 5, 6))
        camera.set_position(1, 1, 1)

    def test_keyboardcamera(self):
        camera = KeyboardCamera(BaseKeys, fov=60, aspect_ratio=1.0, near=1.0, far=100.0)
        camera.mouse_sensitivity = 10.0
        camera.velocity = 10.0
        self.assertEqual(camera.mouse_sensitivity, 10.0)
        self.assertEqual(camera.velocity, 10.0)
        self.assertIsInstance(camera.projection, Projection3D)
        self.assertIsInstance(camera.matrix, glm.mat4)

        camera.key_input(BaseKeys.UP, BaseKeys.ACTION_PRESS, KeyModifiers)

        camera.move_left(True)
        camera.move_right(True)
        camera.move_forward(True)
        camera.move_backward(True)
        camera.move_up(True)
        camera.move_down(True)

        camera.move_state(cam.FORWARD, True)
        camera.rot_state(-17, 4)
