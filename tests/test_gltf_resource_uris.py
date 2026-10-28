import base64
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from PIL import Image

from headless import HeadlessTestCase
from moderngl_window.loaders.scene import gltf2
from moderngl_window.meta import SceneDescription


NAMES = [
    ("mesh data", "mesh%20data"),
    ("grande_sphère", "grande_sph%C3%A8re"),
    ("part#1", "part%231"),
    ("literal%20name", "literal%2520name"),
    ("folder name/mesh", "folder%20name/mesh"),
    ("a+b", "a+b"),
    ("simple", "simple"),
    ("grande_sphère", "grande_sphère"),
]
PIXELS = bytes([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120])


def png_bytes():
    stream = io.BytesIO()
    with Image.frombytes("RGB", (2, 2), PIXELS) as image:
        image.save(stream, format="PNG")
    return stream.getvalue()


@pytest.fixture
def capture_texture(monkeypatch):
    # Exercise real image decoding without requiring a graphics context here.
    class TextureUpload:
        def __init__(self, meta):
            self.meta = meta

        def load(self):
            with self.meta.image as image:
                return image.size, image.tobytes()

    monkeypatch.setattr(gltf2.t2d, "Loader", TextureUpload)


@pytest.mark.parametrize("name,uri", NAMES)
def test_external_buffer_uri(tmp_path, name, uri):
    path = tmp_path / (name + ".bin")
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = b"\x00\x01\x02\x03\x04\x05"
    path.write_bytes(raw)
    meta = gltf2.GLTFMeta(
        tmp_path / "scene.gltf",
        {"asset": {"version": "2.0"}, "buffers": [{"uri": uri + ".bin", "byteLength": len(raw)}]},
        SceneDescription(path="scene.gltf"),
    )
    buffer = meta.buffers[0]
    assert buffer.read(0, len(raw)) == raw
    assert buffer.read(2, 3) == raw[2:5]
    assert buffer.uri == uri + ".bin"


@pytest.mark.parametrize("name,uri", NAMES)
def test_external_image_uri(tmp_path, capture_texture, name, uri):
    path = tmp_path / (name + ".png")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png_bytes())
    image = gltf2.GLTFImage({"uri": uri + ".png"})
    assert image.load(tmp_path) == ((2, 2), PIXELS)
    assert image.uri == uri + ".png"


def test_embedded_buffer_uri(tmp_path):
    raw = b"\x00\x01\x02\xfb\xff"
    uri = "data:application/octet-stream;base64," + base64.b64encode(raw).decode("ascii")
    buffer = gltf2.GLTFBuffer(0, {"uri": uri, "byteLength": len(raw)}, tmp_path)
    assert buffer.read(0, len(raw)) == raw


def test_embedded_image_uri(tmp_path, capture_texture):
    uri = "data:image/png;base64," + base64.b64encode(png_bytes()).decode("ascii")
    assert gltf2.GLTFImage({"uri": uri}).load(tmp_path) == ((2, 2), PIXELS)


def test_buffer_view_image(tmp_path, capture_texture):
    buffer = gltf2.GLTFBuffer(0, {}, tmp_path)
    buffer.data = png_bytes()
    view = gltf2.GLTFBufferView(0, {"buffer": 0, "byteLength": len(buffer.data)})
    view.buffer = buffer
    image = gltf2.GLTFImage({"bufferView": 0, "mimeType": "image/png"})
    image.bufferView = view
    assert image.load(tmp_path) == ((2, 2), PIXELS)


class GltfURIIntegrationTests(HeadlessTestCase):
    def test_scene_with_external_resource_uris(self):
        fixture = Path(__file__).parent / "fixtures/resources/scenes/BoxTextured/glTF"
        raw = (fixture / "BoxTextured0.bin").read_bytes()
        for name, uri in NAMES:
            with self.subTest(uri=uri), TemporaryDirectory() as directory:
                folder = Path(directory)
                resource = folder / name
                resource.parent.mkdir(parents=True, exist_ok=True)
                resource.with_suffix(".bin").write_bytes(raw)
                resource.with_suffix(".png").write_bytes(png_bytes())
                data = json.loads((fixture / "BoxTextured.gltf").read_text())
                data["buffers"][0]["uri"] = uri + ".bin"
                data["images"][0]["uri"] = uri + ".png"
                path = folder / "scene.gltf"
                path.write_text(json.dumps(data))
                scene = gltf2.Loader(SceneDescription(path=str(path))).load()
                self.assertEqual(len(scene.meshes), 1)
                texture = scene.meshes[0].material.mat_texture.texture
                self.assertEqual(texture.size, (2, 2))
                self.assertEqual(texture.read(alignment=1), PIXELS)
