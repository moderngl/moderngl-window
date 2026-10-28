import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from headless import HeadlessTestCase
from moderngl_window.loaders.scene import gltf2
from moderngl_window.meta import SceneDescription


@pytest.mark.parametrize("data", [{}, {"name": "Plain"}, {"pbrMetallicRoughness": {}}])
def test_material_defaults(data):
    material = gltf2.GLTFMaterial(data)
    assert material.name == data.get("name")
    assert material.doubleSided is False
    assert material.baseColorFactor == [1.0, 1.0, 1.0, 1.0]
    assert material.baseColorTexture is None
    assert material.metallicFactor == 1.0
    assert material.emissiveFactor == [0.0, 0.0, 0.0]


@pytest.mark.parametrize("double_sided", [False, True])
def test_explicit_material_values_are_preserved(double_sided):
    data = {
        "name": "Explicit",
        "doubleSided": double_sided,
        "emissiveFactor": [0.1, 0.2, 0.3],
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.0, 0.0, 0.0, 0.0],
            "baseColorTexture": {"index": 0},
            "metallicFactor": 0.0,
        },
    }
    material = gltf2.GLTFMaterial(data)
    assert material.name == "Explicit"
    assert material.doubleSided is double_sided
    assert material.baseColorFactor == [0.0, 0.0, 0.0, 0.0]
    assert material.baseColorTexture == {"index": 0}
    assert material.metallicFactor == 0.0
    assert material.emissiveFactor == [0.1, 0.2, 0.3]


def test_material_default_arrays_are_independent():
    first = gltf2.GLTFMaterial({})
    second = gltf2.GLTFMaterial({})
    first.baseColorFactor[0] = 0.0
    first.emissiveFactor[0] = 1.0
    assert second.baseColorFactor == [1.0, 1.0, 1.0, 1.0]
    assert second.emissiveFactor == [0.0, 0.0, 0.0]


class GltfMaterialIntegrationTests(HeadlessTestCase):
    def test_scene_material_defaults(self):
        fixture = Path(__file__).parent / "fixtures/resources/scenes/BoxTextured/glTF"
        white = [1.0, 1.0, 1.0, 1.0]
        cases = [
            ({}, white, False),
            ({"name": "Plain"}, white, False),
            ({"pbrMetallicRoughness": {}}, white, False),
            ({"pbrMetallicRoughness": {}, "doubleSided": True}, white, True),
            ({"pbrMetallicRoughness": {}, "doubleSided": False}, white, False),
            ({"pbrMetallicRoughness": {"baseColorFactor": [0.0] * 4}}, [0.0] * 4, False),
            (
                {
                    "pbrMetallicRoughness": {"baseColorFactor": [0.2, 0.4, 0.6, 1.0]},
                    "doubleSided": True,
                },
                [0.2, 0.4, 0.6, 1.0],
                True,
            ),
        ]
        with TemporaryDirectory() as directory:
            folder = Path(directory)
            (folder / "BoxTextured0.bin").write_bytes((fixture / "BoxTextured0.bin").read_bytes())
            path = folder / "scene.gltf"
            for material, color, double_sided in cases:
                with self.subTest(material=material):
                    data = json.loads((fixture / "BoxTextured.gltf").read_text())
                    data["materials"] = [material]
                    data["images"] = []
                    data["textures"] = []
                    data["samplers"] = []
                    path.write_text(json.dumps(data))
                    scene = gltf2.Loader(SceneDescription(path=str(path))).load()
                    try:
                        self.assertEqual(len(scene.meshes), 1)
                        self.assertEqual(len(scene.materials), 1)
                        loaded = scene.materials[0]
                        self.assertIs(scene.meshes[0].material, loaded)
                        self.assertEqual(list(loaded.color), color)
                        self.assertIs(loaded.double_sided, double_sided)
                        self.assertIsNone(loaded.mat_texture)
                    finally:
                        scene.release()
