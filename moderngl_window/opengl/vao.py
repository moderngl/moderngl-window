from typing import List

import numpy
import moderngl
import moderngl_window as mglw
from moderngl_window.opengl import types


# For sanity checking draw modes when creating the VAO
DRAW_MODES = {
    moderngl.TRIANGLES: "TRIANGLES",
    moderngl.TRIANGLE_FAN: "TRIANGLE_FAN",
    moderngl.TRIANGLE_STRIP: "TRIANGLE_STRIP",
    moderngl.TRIANGLES_ADJACENCY: "TRIANGLES_ADJACENCY",
    moderngl.TRIANGLE_STRIP_ADJACENCY: "TRIANGLE_STRIP_ADJACENCY",
    moderngl.POINTS: "POINTS",
    moderngl.LINES: "LINES",
    moderngl.LINE_STRIP: "LINE_STRIP",
    moderngl.LINE_LOOP: "LINE_LOOP",
    moderngl.LINES_ADJACENCY: "LINES_ADJACENCY",
}


class BufferInfo:
    """Container for a vbo with additional information"""

    def __init__(
        self,
        buffer: moderngl.Buffer,
        buffer_format: str,
        attributes=None,
        per_instance=False,
    ):
        """
        :param buffer: The vbo object
        :param format: The format of the buffer
        """
        self.buffer = buffer
        self.attrib_formats = types.parse_attribute_formats(buffer_format)
        self.attributes = attributes
        self.per_instance = per_instance

        # Sanity check byte size
        if self.buffer.size % self.vertex_size != 0:
            raise VAOError(
                "Buffer with type {} has size not aligning with {}. Remainder: {}".format(
                    buffer_format, self.vertex_size, self.buffer.size % self.vertex_size
                )
            )

        self.vertices = self.buffer.size // self.vertex_size

    @property
    def vertex_size(self) -> int:
        return sum(f.bytes_total for f in self.attrib_formats)

    def content(self, attributes: List[str]):
        """Build content tuple for the buffer"""
        formats = []
        attrs = []
        for attrib_format, attrib in zip(self.attrib_formats, self.attributes):

            if attrib not in attributes:
                formats.append(attrib_format.pad_str())
                continue

            formats.append(attrib_format.format)
            attrs.append(attrib)

            attributes.remove(attrib)

        if not attrs:
            return None

        return (
            self.buffer,
            "{}{}".format(" ".join(formats), "/i" if self.per_instance else ""),
            *attrs,
        )

    def has_attribute(self, name):
        return name in self.attributes


class VAO:
    """
    Represents a vertex array object.

    This is a wrapper class over ``moderngl.VertexArray`` to make interactions
    with programs/shaders simpler. Named buffers are added correspoding with
    attribute names in a vertex shader. When rendering the VAO an internal
    ``moderngl.VertextArray`` is created automatically mapping the named buffers
    compatible with the supplied program. This program is cached internally.

    The shader program doesn't need to use all the buffers registered in
    this wrapper. When a subset is used only the used buffers are mapped
    and the appropriate padding is calculated when interleaved data is used.

    You are not required to use this class, but most methods in the
    system creating vertexbuffers will return this type. You can obtain
    a single ``moderngl.VertexBuffer`` instance by calling :py:meth:`VAO.instance`
    method if you prefer to work directly on moderngl instances.

    Example::

        # Separate buffers
        vao = VAO(name="test", mode=moderngl.POINTS)
        vao.buffer(positions, '3f', ['in_position'])
        vao.buffer(velocities, '3f', ['in_velocities'])

        # Interleaved
        vao = VAO(name="test", mode=moderngl.POINTS)
        vao.buffer(interleaved_data, '3f 3f', ['in_position', 'in_velocities'])

    .. code:: glsl

        # GLSL vertex shader in attributes
        in vec3 in_position;
        in vec3 in_velocities;

    """

    def __init__(self, name="", mode=moderngl.TRIANGLES):
        """Create and empty VAO with a name and default render mode.

        Example::

            VAO(name="cube", mode=moderngl.TRIANGLES)

        Keyword Args:
            name (str): Optional name for debug purposes
            mode (int): Default draw mode
        """
        self.name = name
        self.mode = mode

        try:
            DRAW_MODES[self.mode]
        except KeyError:
            raise VAOError("Invalid draw mode. Options are {}".format(DRAW_MODES.values()))

        self._buffers = []
        self._index_buffer = None
        self._index_element_size = None

        self.vertex_count = 0
        self.vaos = {}

    @property
    def ctx(self):
        """moderngl.Context: The actite moderngl context"""
        return mglw.ctx()

    def render(self, program: moderngl.Program, mode=None, vertices=-1, first=0, instances=1):
        """Render the VAO.

        An internal ``moderngl.VertexBuffer`` with compatible buffer bindings
        is automatically created on the fly and cached internally.

        Args:
            program: The ``moderngl.Program``
        Keyword Args:
            mode: Override the draw mode (``TRIANGLES`` etc)
            vertices (int): The number of vertices to transform
            first (int): The index of the first vertex to start with
            instances (int): The number of instances
        """
        vao = self.instance(program)

        if mode is None:
            mode = self.mode

        vao.render(mode, vertices=vertices, first=first, instances=instances)

    def render_indirect(self, program: moderngl.Program, buffer, mode=None, count=-1, *, first=0):
        """
        The render primitive (mode) must be the same as the input primitive of the
        GeometryShader.

        The draw commands are 5 integers:
        (count, instanceCount, firstIndex, baseVertex, baseInstance).

        Args:
            program: The ``moderngl.Program``
            buffer: The ``moderngl.Buffer`` containing indirect draw commands
        Keyword Args:
            mode (int): By default :py:data:`TRIANGLES` will be used.
            count (int): The number of draws.
            first (int): The index of the first indirect draw command.
        """
        vao = self.instance(program)

        if mode is None:
            mode = self.mode

        vao.render_indirect(buffer, mode=mode, count=count, first=first)

    def transform(
        self,
        program: moderngl.Program,
        buffer: moderngl.Buffer,
        mode=None,
        vertices=-1,
        first=0,
        instances=1,
    ):
        """Transform vertices. Stores the output in a single buffer.

        Args:
            program: The ``moderngl.Program``
            buffer: The ``moderngl.buffer`` to store the output
        Keyword Args:
            mode: Draw mode (for example ``moderngl.POINTS``)
            vertices (int): The number of vertices to transform
            first (int): The index of the first vertex to start with
            instances (int): The number of instances
        """
        vao = self.instance(program)

        if mode is None:
            mode = self.mode

        vao.transform(buffer, mode=mode, vertices=vertices, first=first, instances=instances)

    def buffer(self, buffer, buffer_format: str, attribute_names: List[str]):
        """Register a buffer/vbo for the VAO. This can be called multiple times.
        adding multiple buffers (interleaved or not).

        Args:
            buffer:
                The buffer data. Can be ``numpy.array``, ``moderngl.Buffer`` or ``bytes``.
            buffer_format (str):
                The format of the buffer. (eg. ``3f 3f`` for interleaved positions and normals).
            attribute_names:
                A list of attribute names this buffer should map to.
        Returns:
            The ``moderngl.Buffer`` instance object. This is handy when providing ``bytes``
            and ``numpy.array``.
        """
        if not isinstance(attribute_names, list):
            attribute_names = [
                attribute_names,
            ]

        if type(buffer) not in [moderngl.Buffer, numpy.ndarray, bytes]:
            raise VAOError(
                (
                    "buffer parameter must be a moderngl.Buffer, numpy.ndarray or bytes instance"
                    "(not {})".format(type(buffer))
                )
            )

        if isinstance(buffer, numpy.ndarray):
            buffer = self.ctx.buffer(buffer.tobytes())

        if isinstance(buffer, bytes):
            buffer = self.ctx.buffer(data=buffer)

        formats = buffer_format.split()
        if len(formats) != len(attribute_names):
            raise VAOError(
                "Format '{}' does not describe attributes {}".format(buffer_format, attribute_names)
            )

        self._buffers.append(BufferInfo(buffer, buffer_format, attribute_names))
        self.vertex_count = self._buffers[-1].vertices

        return buffer

    def index_buffer(self, buffer, index_element_size=4):
        """Set the index buffer for this VAO.

        Args:
            buffer: ``moderngl.Buffer``, ``numpy.array`` or ``bytes``
        Keyword Args:
            index_element_size (int): Byte size of each element. 1, 2 or 4
        """
        if type(buffer) not in [moderngl.Buffer, numpy.ndarray, bytes]:
            raise VAOError(
                "buffer parameter must be a moderngl.Buffer, numpy.ndarray or bytes instance"
            )

        if isinstance(buffer, numpy.ndarray):
            buffer = self.ctx.buffer(buffer.tobytes())

        if isinstance(buffer, bytes):
            buffer = self.ctx.buffer(data=buffer)

        self._index_buffer = buffer
        self._index_element_size = index_element_size

    def instance(self, program: moderngl.Program) -> moderngl.VertexArray:
        """Obtain the ``moderngl.VertexArray`` instance for the program.

        The instance is only created once and cached internally.

        Args:
            program (moderngl.Program): The program

        Returns:
            ``moderngl.VertexArray``: instance
        """
        vao = self.vaos.get(program.glo)
        if vao:
            return vao

        program_attributes = [
            name
            for name, attr in program._members.items()
            if isinstance(attr, moderngl.Attribute) and not attr.name.startswith("gl_")
        ]

        # Make sure all attributes are covered
        for attrib_name in program_attributes:

            # Do we have a buffer mapping to this attribute?
            if not sum(buffer.has_attribute(attrib_name) for buffer in self._buffers):
                raise VAOError(
                    (
                        "VAO {} doesn't have attribute {} for program {}.\n"
                        "Program attributes: {}.\n"
                        "VAO attributes: {}"
                    ).format(
                        self.name,
                        attrib_name,
                        program,
                        program_attributes,
                        [attr for buff in self._buffers for attr in buff.attributes],
                    )
                )

        vao_content = []

        # Pick out the attributes we can actually map
        for buffer in self._buffers:
            content = buffer.content(program_attributes)
            if content:
                vao_content.append(content)

        # Any attribute left is not accounted for
        if program_attributes:
            raise VAOError(
                "Did not find a buffer mapping for {}".format([n for n in program_attributes])
            )

        # Create the vao
        if self._index_buffer:
            vao = self.ctx.vertex_array(
                program,
                vao_content,
                self._index_buffer,
                self._index_element_size,
            )
        else:
            vao = self.ctx.vertex_array(program, vao_content)

        self.vaos[program.glo] = vao
        return vao

    def release(self, buffer=True):
        """Destroy all internally cached vaos and release all buffers.

        Keyword Args:
            buffers (bool): also release buffers
        """
        for _, vao in self.vaos.items():
            vao.release()

        self.vaos = {}

        if buffer:
            for buff in self._buffers:
                buff.buffer.release()

            if self._index_buffer:
                self._index_buffer.release()

        self._buffers = []

    def get_buffer_by_name(self, name: str) -> BufferInfo:
        """Get the BufferInfo associated with a specific attribute name

        If no buffer is associated with the name `None` will be returned.

        Args:
            name (str): Name of the mapped attribute
        Returns:
            BufferInfo: BufferInfo instance
        """
        for buffer in self._buffers:
            if name in buffer.attributes:
                return buffer

        return None


class VAOError(Exception):
    pass
