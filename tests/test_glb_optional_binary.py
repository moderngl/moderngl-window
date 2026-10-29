import base64
import json
import shutil
import struct
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from headless import HeadlessTestCase
from moderngl_window.loaders.scene import gltf2
from moderngl_window.meta import SceneDescription


def write_glb(path, data, binary=None, tail=None):
    content = json.dumps(data).encode()
    content += b" " * (-len(content) % 4)
    chunks = struct.pack("<I4s", len(content), b"JSON") + content
    if binary is not None:
        binary += b"\0" * (-len(binary) % 4)
        chunks += struct.pack("<I4s", len(binary), b"BIN\0") + binary
    if tail is not None:
        chunks += tail
    path.write_bytes(struct.pack("<4sII", b"glTF", 2, 12 + len(chunks)) + chunks)


def parse_glb(path):
    loader = gltf2.Loader(SceneDescription(path=str(path)))
    loader.path = path
    loader.load_glb()
    return loader.gltf


def test_glb_without_any_buffers(tmp_path):
    path = tmp_path / "nodes.glb"
    data = {"asset": {"version": "2.0"}, "nodes": [{"name": "root"}]}
    write_glb(path, data)
    loaded = parse_glb(path)
    assert loaded.data == data
    assert loaded.nodes[0].name == "root"
    assert loaded.buffers == []


@pytest.mark.parametrize("storage", ["external", "data", "binary"])
def test_glb_buffer_contents(tmp_path, storage):
    path = tmp_path / "buffer.glb"
    payload = struct.pack("<3f", 1.0, 2.0, 3.0)
    buffer = {"byteLength": len(payload)}
    if storage == "external":
        buffer["uri"] = "buffer.bin"
        (tmp_path / "buffer.bin").write_bytes(payload)
    elif storage == "data":
        buffer["uri"] = "data:application/octet-stream;base64," + base64.b64encode(payload).decode()
    data = {"asset": {"version": "2.0"}, "buffers": [buffer]}
    write_glb(path, data, binary=payload if storage == "binary" else None)
    assert parse_glb(path).buffers[0].read(byte_length=len(payload)) == payload


@pytest.mark.parametrize("length", range(1, 8))
def test_incomplete_binary_chunk_header_is_not_missing(tmp_path, length):
    path = tmp_path / "truncated.glb"
    header = struct.pack("<I4s", 4, b"BIN\0")
    write_glb(path, {"asset": {"version": "2.0"}}, tail=header[:length])
    with pytest.raises(ValueError, match="binary chunk header"):
        parse_glb(path)


def test_incomplete_binary_chunk_data_is_rejected(tmp_path):
    path = tmp_path / "truncated.glb"
    data = {"asset": {"version": "2.0"}, "buffers": [{"byteLength": 4}]}
    write_glb(path, data, tail=struct.pack("<I4s", 4, b"BIN\0") + b"\0\0")
    with pytest.raises(ValueError, match="binary chunk data"):
        parse_glb(path)


def test_required_binary_chunk_cannot_be_omitted(tmp_path):
    path = tmp_path / "missing.glb"
    data = {"asset": {"version": "2.0"}, "buffers": [{"byteLength": 4}]}
    write_glb(path, data)
    with pytest.raises(ValueError, match="requires a BIN chunk"):
        parse_glb(path)


def test_unexpected_chunk_type_remains_rejected(tmp_path):
    path = tmp_path / "unexpected.glb"
    write_glb(path, {"asset": {"version": "2.0"}}, tail=struct.pack("<I4s", 0, b"JSON"))
    with pytest.raises(ValueError, match="Expected BIN chunk"):
        parse_glb(path)


class GlbSceneTests(HeadlessTestCase):
    def test_scene_with_optional_binary_chunk(self):
        fixture = Path(__file__).parent / "fixtures/resources/scenes/BoxTextured/glTF"
        original = json.loads((fixture / "BoxTextured.gltf").read_text())
        payload = (fixture / "BoxTextured0.bin").read_bytes()
        with TemporaryDirectory() as directory:
            folder = Path(directory)
            shutil.copyfile(fixture / "CesiumLogoFlat.png", folder / "CesiumLogoFlat.png")
            (folder / "BoxTextured0.bin").write_bytes(payload)
            path = folder / "scene.glb"
            for storage in ("external", "data", "binary"):
                with self.subTest(storage=storage):
                    data = json.loads(json.dumps(original))
                    if storage == "data":
                        data["buffers"][0]["uri"] = (
                            "data:application/octet-stream;base64,"
                            + base64.b64encode(payload).decode()
                        )
                    elif storage == "binary":
                        del data["buffers"][0]["uri"]
                    write_glb(path, data, binary=payload if storage == "binary" else None)
                    scene = gltf2.Loader(SceneDescription(path=str(path))).load()
                    try:
                        self.assertEqual(len(scene.meshes), 1)
                        self.assertEqual(scene.meshes[0].vao.vertex_count, 24)
                        self.assertEqual(len(scene.materials), 1)
                        self.assertIsNotNone(scene.materials[0].mat_texture.texture)
                    finally:
                        scene.release()
