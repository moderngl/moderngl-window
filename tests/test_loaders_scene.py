"""
Note: In the future we might want to split this into separate scene loaders
"""
from pathlib import Path

from headless import HeadlessTestCase

from moderngl_window import resources
from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.meta import SceneDescription
from moderngl_window.scene import Scene

resources.register_dir((Path(__file__).parent / 'fixtures' / 'resources').resolve())


class SceneLoadersTestCase(HeadlessTestCase):
    window_size = (16, 16)
    aspect_ratio = 1.0

    def test_wavefront(self):
        """Load wavefront file"""
        scene = resources.scenes.load(SceneDescription(path='scenes/crate/crate.obj'))
        self.assertIsInstance(scene, Scene)

    def test_wavefont_not_found(self):
        """Ensure ImproperlyConfigured is raised when wavefront is not found"""
        with self.assertRaises(ImproperlyConfigured):
            resources.scenes.load(SceneDescription(path='scenes/doesnotexist.obj'))

    def test_gltf(self):
        """Load standard gltf"""
        scene = resources.scenes.load(SceneDescription(path='scenes/BoxTextured/glTF/BoxTextured.gltf'))
        self.assertIsInstance(scene, Scene)

    def test_gltf_binary(self):
        """Load binary gltf"""
        scene = resources.scenes.load(SceneDescription(path='scenes/BoxTextured/glTF-Binary/BoxTextured.glb'))
        self.assertIsInstance(scene, Scene)

    def test_gltf_embedded(self):
        """Load embedded gltf"""
        scene = resources.scenes.load(SceneDescription(path='scenes/BoxTextured/glTF-Embedded/BoxTextured.gltf'))
        self.assertIsInstance(scene, Scene)

    def test_gltf_not_found(self):
        """Attempt to load nonexisting gltf"""
        with self.assertRaises(ImproperlyConfigured):
            resources.scenes.load(SceneDescription(path='scenes/doesnotexist.gltf'))

    def test_stl(self):
        scene = resources.scenes.load(SceneDescription(path='scenes/uplink.stl'))
        self.assertIsInstance(scene, Scene)
