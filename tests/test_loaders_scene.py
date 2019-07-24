"""
Note: In the future we might want to split this into separate scene loaders
"""
from pathlib import Path

from headless import HeadlessTestCase
from moderngl_window import resources
from moderngl_window.meta import SceneDescription
from moderngl_window.scene import Scene

resources.register_dir((Path(__file__).parent / 'fixtures' / 'resources').resolve())


class SceneLoadersTestCase(HeadlessTestCase):
    window_size = (16, 16)
    aspect_ratio = 1.0

    def test_scene_wavefront(self):
        scene = resources.scenes.load(SceneDescription(path='scenes/crate/crate.obj'))
        self.assertIsInstance(scene, Scene)

    def test_scene_gltf(self):
        scene = resources.scenes.load(SceneDescription(path='scenes/BoxTextured/glTF/BoxTextured.gltf'))
        self.assertIsInstance(scene, Scene)

    def test_scene_gltf_binary(self):
        scene = resources.scenes.load(SceneDescription(path='scenes/BoxTextured/glTF-Binary/BoxTextured.glb'))
        self.assertIsInstance(scene, Scene)

    def test_scene_gltf_embedded(self):
        scene = resources.scenes.load(SceneDescription(path='scenes/BoxTextured/glTF-Embedded/BoxTextured.gltf'))
        self.assertIsInstance(scene, Scene)
