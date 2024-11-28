# Spec: https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md#asset
from __future__ import annotations

import base64
import io
import json
import logging
import struct
from collections import namedtuple
from pathlib import Path
from typing import Any, Optional, Union

import glm
import moderngl
import numpy
import numpy.typing as npt
from PIL import Image

import moderngl_window
from moderngl_window.exceptions import ImproperlyConfigured
from moderngl_window.loaders.base import BaseLoader
from moderngl_window.loaders.texture import t2d
from moderngl_window.meta import SceneDescription, TextureDescription
from moderngl_window.opengl.vao import VAO
from moderngl_window.scene import Material, MaterialTexture, Mesh, Node, Scene

logger = logging.getLogger(__name__)

GLTF_MAGIC_HEADER = b"glTF"

# Texture wrap values
REPEAT = 10497
CLAMP_TO_EDGE = 33071
MIRRORED_REPEAT = 33648

# numpy dtype mapping
NP_COMPONENT_DTYPE = {
    5121: numpy.uint8,  # GL_UNSIGNED_BYTE
    5123: numpy.uint16,  # GL_UNSIGNED_SHORT
    5125: numpy.uint32,  # GL_UNSIGNED_INT
    5126: numpy.float32,  # GL_FLOAT
}

ComponentType = namedtuple("ComponentType", ["name", "value", "size"])

COMPONENT_TYPE = {
    5120: ComponentType("BYTE", 5120, 1),
    5121: ComponentType("UNSIGNED_BYTE", 5121, 1),
    5122: ComponentType("SHORT", 5122, 2),
    5123: ComponentType("UNSIGNED_SHORT", 5123, 2),
    5125: ComponentType("UNSIGNED_INT", 5125, 4),
    5126: ComponentType("FLOAT", 5126, 4),
}

# dtype to moderngl buffer format
DTYPE_BUFFER_TYPE = {
    numpy.uint8: "u1",  # GL_UNSIGNED_BYTE
    numpy.uint16: "u2",  # GL_UNSIGNED_SHORT
    numpy.uint32: "u4",  # GL_UNSIGNED_INT
    numpy.float32: "f4",  # GL_FLOAT
}

ACCESSOR_TYPE = {
    "SCALAR": 1,
    "VEC2": 2,
    "VEC3": 3,
    "VEC4": 4,
}


class Loader(BaseLoader):
    """Loader for GLTF 2.0 files"""

    kind = "gltf"
    file_extensions = [
        [".gltf"],
        [".glb"],
    ]
    #: Supported GLTF extensions
    #: https://github.com/KhronosGroup/glTF/tree/master/extensions
    supported_extensions: list[str] = []

    meta: SceneDescription

    def __init__(self, meta: SceneDescription):
        """Initialize loading GLTF 2 scene.

        Supported formats:

        - gltf json format with external resources
        - gltf embedded buffers
        - glb Binary format
        """
        super().__init__(meta)
        self.scenes: list[Scene] = []
        self.nodes: list[Node] = []
        self.meshes: list[list[Mesh]] = []
        self.materials: list[Material] = []
        self.images: list[moderngl.Texture] = []
        self.samplers: list[moderngl.Sampler] = []
        self.textures: list[MaterialTexture] = []

        self.path: Optional[Path] = None
        self.scene: Scene
        self.gltf: GLTFMeta

    def load(self) -> Scene:
        """Load a GLTF 2 scene including referenced textures.

        Returns:
            Scene: The scene instance
        """
        assert self.meta.path is not None, "The path to this resource is empty"
        self.path = self.find_scene(self.meta.path)
        if not self.path:
            raise ImproperlyConfigured("Scene '{}' not found".format(self.meta.path))

        self.scene = Scene(str(self.path))

        # Load gltf json file
        if self.path.suffix == ".gltf":
            self.load_gltf()

        # Load binary gltf file
        if self.path.suffix == ".glb":
            self.load_glb()

        assert self.gltf is not None, "There is a problem with your file, could not load gltf"

        self.gltf.check_version()
        self.gltf.check_extensions(self.supported_extensions)
        self.load_images()
        self.load_samplers()
        self.load_textures()
        self.load_materials()
        self.load_meshes()
        self.load_nodes()

        self.scene.calc_scene_bbox()
        self.scene.prepare()

        return self.scene

    def load_gltf(self) -> None:
        """Loads a gltf json file parsing its contents"""
        with open(str(self.path)) as fd:
            self.gltf = GLTFMeta(str(self.path), json.load(fd), self.meta)

    def load_glb(self) -> None:
        """Loads a binary gltf file parsing its contents"""
        with open(str(self.path), "rb") as fd:
            # Check header
            magic = fd.read(4)
            if magic != GLTF_MAGIC_HEADER:
                raise ValueError(
                    "{} has incorrect header {!r} != {!r}".format(
                        self.path, magic, GLTF_MAGIC_HEADER
                    )
                )

            version = struct.unpack("<I", fd.read(4))[0]
            if version != 2:
                raise ValueError(f"{self.path} has unsupported version {version}")

            # Total file size including headers
            _ = struct.unpack("<I", fd.read(4))[0]  # noqa

            # Chunk 0 - json
            chunk_0_length = struct.unpack("<I", fd.read(4))[0]
            chunk_0_type = fd.read(4)
            if chunk_0_type != b"JSON":
                raise ValueError(
                    "Expected JSON chunk, not {!r} in file {}".format(chunk_0_type, self.path)
                )

            json_meta = fd.read(chunk_0_length).decode()

            # chunk 1 - binary buffer
            chunk_1_length = struct.unpack("<I", fd.read(4))[0]
            chunk_1_type = fd.read(4)
            if chunk_1_type != b"BIN\x00":
                raise ValueError(
                    "Expected BIN chunk, not {!r} in file {}".format(chunk_1_type, self.path)
                )

            self.gltf = GLTFMeta(
                str(self.path),
                json.loads(json_meta),
                self.meta,
                binary_buffer=fd.read(chunk_1_length),
            )

    def load_images(self) -> None:
        """Load images referenced in gltf metadata"""
        for image in self.gltf.images:
            self.images.append(image.load(self.path.parent))

    def load_samplers(self) -> None:
        """Load samplers referenced in gltf metadata"""
        for sampler in self.gltf.samplers:
            # Use a sane default sampler if the sampler data is empty
            # Samplers can simply just be json data: "{}"
            if sampler.minFilter is sampler.magFilter is None:
                self.samplers.append(
                    self.ctx.sampler(
                        filter=(moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR),
                        repeat_x=False,
                        repeat_y=False,
                        anisotropy=16.0,
                    )
                )
            else:
                self.samplers.append(
                    self.ctx.sampler(
                        filter=(sampler.minFilter, sampler.magFilter),
                        repeat_x=sampler.wrapS in [REPEAT, MIRRORED_REPEAT],
                        repeat_y=sampler.wrapT in [REPEAT, MIRRORED_REPEAT],
                        anisotropy=16.0,
                    )
                )

    def load_textures(self) -> None:
        """Load textures referenced in gltf metadata"""
        for texture_meta in self.gltf.textures:
            texture = MaterialTexture()

            if texture_meta.source is not None:
                texture.texture = self.images[texture_meta.source]

            if texture_meta.sampler is not None:
                texture.sampler = self.samplers[texture_meta.sampler]

            self.textures.append(texture)

    def load_meshes(self) -> None:
        """Load meshes referenced in gltf metadata"""
        for meta_mesh in self.gltf.meshes:
            # Returns a list of meshes
            meshes = meta_mesh.load(self.materials)
            self.meshes.append(meshes)

            for mesh in meshes:
                self.scene.meshes.append(mesh)

    def load_materials(self) -> None:
        """Load materials referenced in gltf metadata"""
        # Create material objects
        for meta_mat in self.gltf.materials:
            mat = Material(meta_mat.name)
            mat.color = meta_mat.baseColorFactor or (1.0, 1.0, 1.0, 1.0)
            mat.double_sided = meta_mat.doubleSided

            if meta_mat.baseColorTexture is not None:
                mat.mat_texture = self.textures[meta_mat.baseColorTexture["index"]]

            self.materials.append(mat)
            self.scene.materials.append(mat)

    def load_nodes(self) -> None:
        """Load nodes referenced in gltf metadata"""
        # Start with root nodes in the scene
        for node_id in self.gltf.scenes[0].nodes:
            node = self.load_node(self.gltf.nodes[node_id])
            self.scene.root_nodes.append(node)

    def load_node(self, meta: GLTFNode, parent: Optional[Node] = None) -> Node:
        """Load a single node"""
        # Create the node
        node = Node(name=meta.name)
        self.scene.nodes.append(node)

        if meta.matrix is not None:
            node.matrix = glm.mat4(meta.matrix)

        if meta.mesh is not None:
            # Since we split up meshes with multiple primitives, this can be a list
            # If only one mesh we set it on the node as normal
            if len(self.meshes[meta.mesh]) == 1:
                node.mesh = self.meshes[meta.mesh][0]
            # If multiple meshes we add them as new child node
            elif len(self.meshes[meta.mesh]) > 1:
                for mesh in self.meshes[meta.mesh]:
                    node.add_child(Node(mesh=mesh))

        if meta.camera is not None:
            # FIXME: Use a proper camera class
            node.camera = self.gltf.cameras[meta.camera]

        if parent:
            parent.add_child(node)

        # Follow children
        if meta.has_children:
            for node_id in meta.children:
                self.load_node(self.gltf.nodes[node_id], parent=node)

        return node


class GLTFMeta:
    """Container for gltf metadata"""

    def __init__(
        self,
        path: Union[Path, str],
        data: dict[Any, Any],
        meta: SceneDescription,
        binary_buffer: Optional[bytes] = None,
    ) -> None:
        """
        :param file: GLTF file name loaded
        :param data: Metadata (json loaded)
        :param binary_buffer: Binary buffer when loading glb files
        """
        self.path = Path(path) if isinstance(path, str) else path
        self.data = data
        self.meta = meta

        self.asset = GLTFAsset(data["asset"])
        self.materials = (
            [GLTFMaterial(m) for m in data["materials"]] if data.get("materials") else []
        )
        self.images = [GLTFImage(i) for i in data["images"]] if data.get("images") else []
        self.samplers = [GLTFSampler(s) for s in data["samplers"]] if data.get("samplers") else []
        self.textures = [GLTFTexture(t) for t in data["textures"]] if data.get("textures") else []
        self.scenes = [GLTFScene(s) for s in data["scenes"]] if data.get("scenes") else []
        self.nodes = [GLTFNode(n) for n in data["nodes"]] if data.get("nodes") else []
        self.meshes = [GLTFMesh(m, self.meta) for m in data["meshes"]] if data.get("meshes") else []
        self.cameras = [GLTFCamera(c) for c in data["cameras"]] if data.get("cameras") else []
        self.buffer_views = (
            [GLTFBufferView(i, v) for i, v in enumerate(data["bufferViews"])]
            if data.get("bufferViews")
            else []
        )
        self.buffers = (
            [GLTFBuffer(i, b, self.path.parent) for i, b in enumerate(data["buffers"])]
            if data.get("buffers")
            else []
        )
        self.accessors = (
            [GLTFAccessor(i, a) for i, a in enumerate(data["accessors"])]
            if data.get("accessors")
            else []
        )

        # glb files can contain buffer 0 data
        if binary_buffer:
            self.buffers[0].data = binary_buffer

        self._link_data()

        self.buffers_exist()
        self.images_exist()

    def _link_data(self) -> None:
        """Add references"""
        # accessors -> buffer_views -> buffers
        for acc in self.accessors:
            acc.bufferView = self.buffer_views[acc.bufferViewId]

        for buffer_view in self.buffer_views:
            buffer_view.buffer = self.buffers[buffer_view.bufferId]

        # Link accessors to mesh primitives
        for mesh in self.meshes:
            for primitive in mesh.primitives:
                if primitive.indices is not None:
                    primitive.accessor = self.accessors[primitive.indices]
                for name, value in primitive.attributes.items():
                    primitive.attributes[name] = self.accessors[value]

        # Link buffer views to images
        for image in self.images:
            if image.bufferViewId is not None:
                image.bufferView = self.buffer_views[image.bufferViewId]

    @property
    def version(self) -> str:
        return self.asset.version

    def check_version(self, required: str = "2.0") -> None:
        if not self.version == required:
            msg = (
                f"GLTF Format version is not 2.0. Version states '{self.version}' "
                f"in file {self.path}"
            )
            raise ValueError(msg)

    def check_extensions(self, supported: list[str]) -> None:
        """
        "extensionsRequired": ["KHR_draco_mesh_compression"],
        "extensionsUsed": ["KHR_draco_mesh_compression"]
        """
        extReq = self.data.get("extensionsRequired")
        if extReq is not None:
            for ext in extReq:
                if ext not in supported:
                    raise ValueError(f"Extension {ext} not supported")
        extUse = self.data.get("extensionsUsed")
        if extUse is not None:
            for ext in extUse:
                if ext not in supported:
                    raise ValueError("Extension {ext} not supported")

    def buffers_exist(self) -> None:
        """Checks if the bin files referenced exist"""
        for buff in self.buffers:
            if not buff.is_separate_file:
                continue

            path = self.path.parent / buff.uri
            if not path.exists():
                raise FileNotFoundError(
                    "Buffer {} referenced in {} not found".format(path, self.path)
                )

    def images_exist(self) -> None:
        """checks if the images references in textures exist"""
        pass


class GLTFAsset:
    """Asset Information"""

    def __init__(self, data: dict[str, str]):
        self.version = data.get("version", "")
        self.generator = data.get("generator", "")
        self.copyright = data.get("copyright", "")


class GLTFMesh:
    class Primitives:
        mode: int | None
        accessor: GLTFAccessor | None

        def __init__(self, data: dict[str, Any]):
            self.attributes: dict[str, Any] = data.get("attributes", {})
            self.indices = data.get("indices", 0)
            self.mode = data.get("mode")
            self.material = data.get("material", 0)
            self.accessor = None

    def __init__(self, data: dict[str, Any], meta: SceneDescription):

        self.meta = meta
        self.name = data.get("name", "")
        self.primitives = [GLTFMesh.Primitives(p) for p in data["primitives"]]

    def load(self, materials: list[Material]) -> list[Mesh]:
        name_map = {
            "POSITION": self.meta.attr_names.POSITION,
            "NORMAL": self.meta.attr_names.NORMAL,
            "TEXCOORD_0": self.meta.attr_names.TEXCOORD_0,
            "TANGENT": self.meta.attr_names.TANGENT,
            "JOINTS_0": self.meta.attr_names.JOINTS_0,
            "WEIGHTS_0": self.meta.attr_names.WEIGHTS_0,
            "COLOR_0": self.meta.attr_names.COLOR_0,
        }

        meshes = []

        # Read all primitives as separate meshes for now
        # According to the spec they can have different materials and vertex format
        for primitive in self.primitives:

            vao = VAO(self.name, mode=primitive.mode or moderngl.TRIANGLES)

            # Index buffer
            component_type, index_vbo = self.load_indices(primitive)
            if index_vbo is not None:
                vao.index_buffer(
                    moderngl_window.ctx().buffer(index_vbo.tobytes()),
                    index_element_size=component_type.size,
                )

            attributes = {}
            vbos = self.prepare_attrib_mapping(primitive)

            for vbo_info in vbos:
                dtype, buffer = vbo_info.create()
                vao.buffer(
                    buffer,
                    " ".join(
                        [
                            "{}{}".format(attr[1], DTYPE_BUFFER_TYPE[dtype])
                            for attr in vbo_info.attributes
                        ]
                    ),
                    [name_map[attr[0]] for attr in vbo_info.attributes],
                )

                for attr in vbo_info.attributes:
                    attributes[attr[0]] = {
                        "name": name_map[attr[0]],
                        "components": attr[1],
                        "type": vbo_info.component_type.value,
                    }

            bbox_min, bbox_max = self.get_bbox(primitive)
            meshes.append(
                Mesh(
                    self.name,
                    vao=vao,
                    attributes=attributes,
                    material=(
                        materials[primitive.material] if primitive.material is not None else None
                    ),
                    bbox_min=bbox_min,
                    bbox_max=bbox_max,
                )
            )

        return meshes

    def load_indices(
        self, primitive: Primitives
    ) -> tuple[ComponentType, npt.NDArray[Any]] | tuple[None, None]:
        """Loads the index buffer / polygon list for a primitive"""
        if primitive.indices is None or primitive.accessor is None:
            return None, None

        _, component_type, buffer = primitive.accessor.read()
        return component_type, buffer

    def prepare_attrib_mapping(self, primitive: Primitives) -> list[VBOInfo]:
        """Pre-parse buffer mappings for each VBO to detect interleaved data for a primitive"""
        buffer_info: list[VBOInfo] = []
        for name, accessor in primitive.attributes.items():
            info = VBOInfo(*accessor.info())
            info.attributes.append((name, info.components))

            if buffer_info and buffer_info[-1].buffer_view == info.buffer_view:
                if buffer_info[-1].interleaves(info):
                    buffer_info[-1].merge(info)
                    continue

            buffer_info.append(info)

        return buffer_info

    def get_bbox(self, primitive: Primitives) -> tuple[glm.vec3, glm.vec3]:
        """Get the bounding box for the mesh"""
        accessor = primitive.attributes.get("POSITION")
        return glm.vec3(accessor.min), glm.vec3(accessor.max)


class VBOInfo:
    """Resolved data about each VBO"""

    def __init__(
        self,
        buffer: Optional[GLTFBuffer] = None,
        buffer_view: Optional[GLTFBuffer] = None,
        byte_length: int = 0,
        byte_offset: int = 0,
        component_type: ComponentType = ComponentType("", 0, 0),
        components: int = 0,
        count: int = 0,
    ):
        self.buffer = buffer  # reference to the buffer
        self.buffer_view = buffer_view
        self.byte_length = byte_length  # Raw byte buffer length
        self.byte_offset = byte_offset  # Raw byte offset
        self.component_type = component_type  # Datatype of each component
        self.components = components
        self.count = count  # number of elements of the component type size

        # list of (name, components) tuples
        self.attributes: list[Any] = []

    def interleaves(self, info: VBOInfo) -> bool:
        """Does the buffer interleave with this one?"""
        return bool(info.byte_offset == (self.component_type.size * self.components))

    def merge(self, info: VBOInfo) -> None:
        # NOTE: byte length is the same
        self.components += info.components
        self.attributes += info.attributes

    def create(self) -> tuple[type[object], npt.NDArray[Any]]:
        """Create the VBO"""
        assert self.buffer is not None, "No buffer defined"
        dtype = NP_COMPONENT_DTYPE[self.component_type.value]
        data = numpy.frombuffer(
            self.buffer.read(byte_length=self.byte_length, byte_offset=self.byte_offset),
            count=self.count * self.components,
            dtype=dtype,
        )
        return dtype, data

    def __str__(self) -> str:
        assert self.buffer is not None, "No buffer defined"
        assert self.buffer_view is not None, "No buffer_view defined"
        return (
            "VBOInfo<buffer={}, buffer_view={},\n"
            "        length={}, offset={}, count={}\n"
            "        component_type={}, components={}, \n"
            "        attribs={}".format(
                self.buffer.id,
                self.buffer_view.id,
                self.byte_length,
                self.byte_offset,
                self.count,
                self.component_type.value,
                self.components,
                self.attributes,
            )
        )

    def __repr__(self) -> str:
        return str(self)


class GLTFAccessor:
    def __init__(self, accessor_id: int, data: dict[str, Any]):
        self.id = accessor_id
        self.bufferViewId = data.get("bufferView", 0)
        self.bufferView: GLTFBufferView
        self.byteOffset = data.get("byteOffset", 0)
        self.componentType = COMPONENT_TYPE[data["componentType"]]
        self.count = data.get("count", 1)
        self.min = numpy.array(data.get("min") or [-0.5, -0.5, -0.5], dtype="f4")
        self.max = numpy.array(data.get("max") or [0.5, 0.5, 0.5], dtype="f4")
        self.type = data.get("type", "")

    def read(self) -> tuple[int, ComponentType, npt.NDArray[Any]]:
        """
        Reads buffer data
        :return: component count, component type, data
        """
        # ComponentType helps us determine the datatype
        dtype = NP_COMPONENT_DTYPE[self.componentType.value]
        return (
            ACCESSOR_TYPE[self.type],
            self.componentType,
            self.bufferView.read(
                byte_offset=self.byteOffset,
                dtype=dtype,
                count=self.count * ACCESSOR_TYPE[self.type],
            ),
        )

    def info(self) -> tuple[GLTFBuffer, GLTFBufferView, int, int, ComponentType, int, int]:
        """
        Get underlying buffer info for this accessor
        :return: buffer, byte_length, byte_offset, component_type, count
        """
        buffer, byte_length, byte_offset = self.bufferView.info(byte_offset=self.byteOffset)
        return (
            buffer,
            self.bufferView,
            byte_length,
            byte_offset,
            self.componentType,
            ACCESSOR_TYPE[self.type],
            self.count,
        )


class GLTFBufferView:
    def __init__(self, view_id: int, data: dict[str, Any]):
        self.id = view_id
        self.bufferId = data.get("buffer", 0)
        self.buffer: GLTFBuffer
        self.byteOffset = data.get("byteOffset", 0)
        self.byteLength = data.get("byteLength", 0)
        self.byteStride = data.get("byteStride", 0)
        # Valid: 34962 (ARRAY_BUFFER) and 34963 (ELEMENT_ARRAY_BUFFER) or None

    def read(
        self, byte_offset: int = 0, dtype: Optional[type[object]] = None, count: int = 0
    ) -> npt.NDArray[Any]:
        data = self.buffer.read(
            byte_offset=byte_offset + self.byteOffset,
            byte_length=self.byteLength,
        )
        vbo = numpy.frombuffer(data, count=count, dtype=dtype)
        return vbo

    def read_raw(self) -> bytes:
        return self.buffer.read(byte_length=self.byteLength, byte_offset=self.byteOffset)

    def info(self, byte_offset: int = 0) -> tuple[GLTFBuffer, int, int]:
        """
        Get the underlying buffer info
        :param byte_offset: byte offset from accessor
        :return: buffer, byte_length, byte_offset
        """
        return self.buffer, self.byteLength, byte_offset + self.byteOffset


class GLTFBuffer:
    def __init__(self, buffer_id: int, data: dict[str, str], path: Path):
        self.id = buffer_id
        self.path = path
        self.byteLength = data.get("byteLength")
        uri = data.get("uri")
        if uri is None:
            uri = ""
        self.uri = uri
        self.data = b""

    @property
    def has_data_uri(self) -> bool:
        """Is data embedded in json?"""
        if self.uri == "":
            return False

        return self.uri.startswith("data:")

    @property
    def is_separate_file(self) -> bool:
        """Buffer represents an independent bin file?"""
        return self.uri is not None and not self.has_data_uri

    def open(self) -> None:
        if self.data != b"":
            return

        if self.has_data_uri:
            self.data = base64.b64decode(self.uri[self.uri.find(",") + 1 :])
            return

        with open(str(self.path / (self.uri if self.uri is not None else "")), "rb") as fd:
            self.data = fd.read()

    def read(self, byte_offset: int = 0, byte_length: int = 0) -> bytes:
        self.open()
        return self.data[byte_offset : byte_offset + byte_length]


class GLTFScene:
    def __init__(self, data: dict[str, list[int]]):
        self.nodes = data["nodes"]


class GLTFNode:
    def __init__(self, data: dict[str, Any]) -> None:
        self.name = data.get("name")
        self.children = data.get("children")
        self.matrix = data.get("matrix")
        self.mesh = data.get("mesh")
        self.camera = data.get("camera")

        self.translation = data.get("translation")
        self.rotation = data.get("rotation")
        self.scale = data.get("scale")

        if self.matrix is not None:
            self.matrix = glm.mat4(*self.matrix)
        else:
            self.matrix = glm.mat4()

        if self.translation is not None:
            self.matrix = self.matrix * glm.translate(glm.vec3(*self.translation))

        if self.rotation is not None:
            quat = glm.quat(
                x=self.rotation[0],
                y=self.rotation[1],
                z=self.rotation[2],
                w=self.rotation[3],
            )
            self.matrix = self.matrix * glm.mat4(quat)

        if self.scale is not None:
            self.matrix = self.matrix * glm.scale(self.scale)

    @property
    def has_children(self) -> bool:
        return self.children is not None and len(self.children) > 0

    @property
    def is_resource_node(self) -> bool:
        """Is this just a reference node to a resource?"""
        return self.camera is not None or self.mesh is not None


class GLTFMaterial:
    def __init__(self, data: dict[str, Any]):
        self.name = data["name"]
        # Defaults to true if not defined
        self.doubleSided = data.get("doubleSided") or True

        pbr = data["pbrMetallicRoughness"]
        self.baseColorFactor = pbr.get("baseColorFactor")
        self.baseColorTexture = pbr.get("baseColorTexture")
        self.metallicFactor = pbr.get("metallicFactor")
        self.emissiveFactor = data.get("emissiveFactor")


class GLTFImage:
    """
    Represent texture data.
    May be a file, embedded data or pointer to data in bufferview
    """

    def __init__(self, data: dict[str, Any]):
        self.uri = data.get("uri")
        self.bufferViewId = data.get("bufferView")
        self.bufferView = None
        self.mimeType = data.get("mimeType")

    def load(self, path: Path) -> moderngl.Texture:
        # data:image/png;base64,iVBOR

        # Image is stored in bufferView
        if self.bufferView is not None:
            image = Image.open(io.BytesIO(self.bufferView.read_raw()))
        # Image is embedded
        elif self.uri and self.uri.startswith("data:"):
            data = self.uri[self.uri.find(",") + 1 :]
            image = Image.open(io.BytesIO(base64.b64decode(data)))
            logger.info("Loading embedded image")
        else:
            path = path / Path(self.uri if self.uri is not None else "")
            logger.info("Loading: %s", self.uri)
            image = Image.open(path)

        texture = t2d.Loader(
            TextureDescription(
                label="gltf",
                image=image,
                flip=False,
                mipmap=True,
                anisotropy=16.0,
            )
        ).load()

        return texture


class GLTFTexture:
    def __init__(self, data: dict[str, int]):
        self.sampler = data["sampler"]
        self.source = data["source"]


class GLTFSampler:
    def __init__(self, data: dict[str, int]):
        self.magFilter = data["magFilter"]
        self.minFilter = data["minFilter"]
        self.wrapS = data["wrapS"]
        self.wrapT = data["wrapT"]


class GLTFCamera:
    def __init__(self, data: dict[str, str]):
        self.data = data
        # "perspective": {
        #     "aspectRatio": 1.0,
        #     "yfov": 0.266482561826706,
        #     "zfar": 1000000.0,
        #     "znear": 0.04999999701976776
        # },
        # "type": "perspective"
