import io
import logging
import os
from pathlib import Path

import moderngl
import numpy
import pywavefront
from pywavefront import cache
from pywavefront.obj import ObjParser

from moderngl_window import resources
from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.geometry.attributes import AttributeNames
from moderngl_window.loaders.base import BaseLoader
from moderngl_window.meta import SceneDescription, TextureDescription
from moderngl_window.opengl.vao import VAO
from moderngl_window.resources.decorators import texture_dirs
from moderngl_window.scene import Material, MaterialTexture, Mesh, Node, Scene

logger = logging.getLogger(__name__)


def translate_buffer_format(
    vertex_format: str, attr_names: AttributeNames
) -> tuple[str, list[str], list[tuple[str, str, int]]]:
    """Translate the buffer format"""
    buffer_format = []
    attributes = []
    mesh_attributes = []

    if "T2F" in vertex_format:
        buffer_format.append("2f")
        attributes.append(attr_names.TEXCOORD_0)
        mesh_attributes.append(("TEXCOORD_0", attr_names.TEXCOORD_0, 2))

    if "C3F" in vertex_format:
        buffer_format.append("3f")
        attributes.append(attr_names.COLOR_0)
        mesh_attributes.append(("COLOR_0", attr_names.COLOR_0, 3))

    if "N3F" in vertex_format:
        buffer_format.append("3f")
        attributes.append(attr_names.NORMAL)
        mesh_attributes.append(("NORMAL", attr_names.NORMAL, 3))

    buffer_format.append("3f")
    attributes.append(attr_names.POSITION)
    mesh_attributes.append(("POSITION", attr_names.POSITION, 3))

    return " ".join(buffer_format), attributes, mesh_attributes


class VAOCacheLoader(cache.CacheLoader):
    """Load geometry data directly into vaos"""

    attr_names: AttributeNames

    def load_vertex_buffer(
        self, fd: io.TextIOWrapper, material: pywavefront.material.Material, length: int
    ) -> None:
        buffer_format, attributes, mesh_attributes = translate_buffer_format(
            material.vertex_format, self.attr_names
        )

        vao = VAO(material.name, mode=moderngl.TRIANGLES)
        # FIXME: Are we actually reading from text or byte stream here?
        vao.buffer(fd.read(length), buffer_format, attributes)

        setattr(material, "vao", vao)
        setattr(material, "buffer_format", buffer_format)
        setattr(material, "attributes", attributes)
        setattr(material, "mesh_attributes", mesh_attributes)


ObjParser.cache_loader_cls = VAOCacheLoader


class Loader(BaseLoader):
    """Load wavefront/obj files"""

    kind = "wavefront"
    file_extensions = [
        [".obj"],
        [".obj", ".gz"],
        [".bin"],
    ]
    meta: SceneDescription

    def __init__(self, meta: SceneDescription):
        super().__init__(meta)

    def load(self) -> Scene:
        """Loads a wavefront/obj file including materials and textures

        Returns:
            Scene: The Scene instance
        """
        path = self.find_scene(Path(self.meta.path if self.meta.path is not None else ""))
        logger.info("loading %s", path)

        if not path:
            raise ImproperlyConfigured("Scene '{}' not found".format(self.meta.path))

        if path.suffix == ".bin":
            path = path.parent / path.stem

        VAOCacheLoader.attr_names = self.meta.attr_names

        data = pywavefront.Wavefront(str(path), create_materials=True, cache=self.meta.cache)
        scene = Scene(
            self.meta.resolved_path.as_posix() if self.meta.resolved_path is not None else ""
        )
        texture_cache: dict[str, pywavefront.material.Material] = {}

        for _, mat in data.materials.items():
            mesh = Mesh(mat.name)

            # Traditional loader
            if mat.vertices:
                buffer_format, attributes, mesh_attributes = translate_buffer_format(
                    mat.vertex_format, self.meta.attr_names
                )
                vbo = numpy.array(mat.vertices, dtype="f4")

                vao = VAO(mat.name, mode=moderngl.TRIANGLES)
                vao.buffer(vbo, buffer_format, attributes)
                mesh.vao = vao

                for attrs in mesh_attributes:
                    mesh.add_attribute(*attrs)

            # Binary cache loader
            elif hasattr(mat, "vao"):
                mesh = Mesh(mat.name)
                mesh.vao = mat.vao
                for attrs in mat.mesh_attributes:
                    mesh.add_attribute(*attrs)
            else:
                # Empty
                continue

            scene.meshes.append(mesh)

            mesh.material = Material(mat.name)
            scene.materials.append(mesh.material)
            mesh.material.color = mat.diffuse

            if mat.texture:
                # A texture can be referenced multiple times, so we need to cache loaded ones
                texture = texture_cache.get(mat.texture.path)
                if not texture:
                    # HACK: pywavefront only give us an absolute path
                    rel_path = os.path.relpath(mat.texture.find(), str(path.parent))
                    logger.info("Loading: %s", rel_path)
                    with texture_dirs([path.parent]):
                        texture = resources.textures.load(
                            TextureDescription(
                                label=rel_path,
                                path=rel_path,
                                mipmap=True,
                                anisotropy=16.0,
                            )
                        )
                    texture_cache[rel_path] = texture

                mesh.material.mat_texture = MaterialTexture(
                    texture=texture,
                    sampler=None,
                )

            node = Node(mesh=mesh)
            scene.root_nodes.append(node)

        # Not supported yet for obj
        # self.calc_scene_bbox()
        scene.prepare()

        return scene
