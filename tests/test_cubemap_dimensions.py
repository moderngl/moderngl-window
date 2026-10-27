"""Cubemap faces need matching square dimensions, not just equal byte counts."""

import tempfile
from pathlib import Path

import pytest
from headless import HeadlessTestCase
from PIL import Image

from moderngl_window import resources
from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.loaders.texture.cube import FaceInfo, Loader
from moderngl_window.meta import TextureDescription


@pytest.mark.parametrize("face_index", range(6))
@pytest.mark.parametrize("size", [(8, 2), (2, 8)])
def test_rectangular_face_with_equal_byte_count(face_index, size):
    faces = [FaceInfo(4, 4, bytes(64), 4) for _ in range(6)]
    faces[face_index] = FaceInfo(*size, bytes(64), 4)
    with pytest.raises(ImproperlyConfigured):
        Loader(TextureDescription(kind="cube"))._validate(faces)


@pytest.mark.parametrize("components", [3, 4])
@pytest.mark.parametrize("size", [2, 4])
def test_equal_square_faces(size, components):
    faces = [FaceInfo(size, size, bytes(size * size * components), components)] * 6
    assert Loader(TextureDescription(kind="cube"))._validate(faces) == components


class CubemapDimensionTestCase(HeadlessTestCase):
    def _description(self, directory, malformed=False):
        paths = {}
        for index, name in enumerate(("pos_x", "neg_x", "pos_y", "neg_y", "pos_z", "neg_z")):
            path = Path(directory) / (name + ".png")
            size = (8, 2) if malformed and name == "pos_y" else (4, 4)
            with Image.new("RGBA", size, (index, index + 1, index + 2, 255)) as image:
                image.save(path)
            paths[name] = str(path)
        return TextureDescription(kind="cube", **paths)

    def test_mismatched_face_rejected_before_upload(self):
        with tempfile.TemporaryDirectory() as directory:
            description = self._description(directory, malformed=True)
            with self.assertRaises(ImproperlyConfigured):
                texture = resources.textures.load(description)
                texture.release()

    def test_matching_faces_preserve_pixels(self):
        with tempfile.TemporaryDirectory() as directory:
            texture = resources.textures.load(self._description(directory))
            try:
                self.assertEqual(texture.size, (4, 4))
                for index in range(6):
                    self.assertEqual(
                        texture.read(index), bytes((index, index + 1, index + 2, 255)) * 16
                    )
            finally:
                texture.release()
