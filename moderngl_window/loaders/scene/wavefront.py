import logging
import os

import numpy

import pywavefront
from pywavefront import cache
from pywavefront.obj import ObjParser

import moderngl
from moderngl_window.loaders.base import BaseLoader
from moderngl_window.opengl.vao import VAO
from moderngl_window import resources
from moderngl_window.resources.decorators import texture_dirs
from moderngl_window.meta import SceneDescription, TextureDescription
from moderngl_window.scene import Material, MaterialTexture, Mesh, Node, Scene
from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.geometry.attributes import AttributeNames


logger = logging.getLogger(__name__)


def translate_buffer_format(vertex_format: str, attr_names: AttributeNames):
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

    attr_names = None

    def load_vertex_buffer(self, fd, material, length):
        buffer_format, attributes, mesh_attributes = translate_buffer_format(
            material.vertex_format, self.attr_names
        )

        vao = VAO(material.name, mode=moderngl.TRIANGLES)
        vao.buffer(fd.read(length), buffer_format, attributes)

        setattr(material, "vao", vao)
        setattr(material, "buffer_format", buffer_format)
        setattr(material, "attributes", attributes)
        setattr(material, "mesh_attributes", mesh_attributes)


ObjParser.cache_loader_cls = VAOCacheLoader


class Loader(BaseLoader):
    """Loade wavefront/obj files"""

    kind = "wavefront"
    file_extensions = [
        [".obj"],
        [".obj", ".gz"],
        [".bin"],
    ]

    def __init__(self, meta: SceneDescription):
        super().__init__(meta)

    def load(self):
        """Loads a wavefront/obj file including materials and textures

        Returns:
            Scene: The Scene instance
        """
        path = self.find_scene(self.meta.path)
        logger.info("loading %s", path)

        if not path:
            raise ImproperlyConfigured("Scene '{}' not found".format(self.meta.path))

        if path.suffix == ".bin":
            path = path.parent / path.stem

        VAOCacheLoader.attr_names = self.meta.attr_names

        data = pywavefront.Wavefront(str(path), create_materials=True, cache=self.meta.cache)
        scene = Scene(self.meta.resolved_path)
        texture_cache = {}

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
