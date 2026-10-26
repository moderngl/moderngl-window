import moderngl
import numpy
from headless import HeadlessTestCase
from unittest.mock import PropertyMock, patch

from moderngl_window.opengl.vao import VAO, BufferInfo, VAOError


class VaoTestCase(HeadlessTestCase):

    def createProgram(self):
        return self.ctx.program(
            vertex_shader="""
            #version 330

            in vec3 position;
            in vec3 normal;
            out vec3 v_normal;

            void main() {
                gl_Position = vec4(position, 1.0);
                v_normal = normalize(normal);
            }
            """,
            fragment_shader="""
            #version 330

            out vec4 fragColor;
            in vec3 v_normal;

            void main() {
                float col = length(v_normal);
                fragColor = vec4(col);
            }
            """,
        )

    def test_create(self):
        mesh = VAO("test", mode=moderngl.LINES)
        mesh.buffer(
            numpy.array([0.0, 0.0, 0.0, 1.0, 1.0, 1.0], dtype="f4"), "3f", "position"
        )
        mesh.buffer(
            numpy.array([0.0, 0.0, 1.0, 1.0, 0.0, 1.0], dtype="f4"), "3f", "normal"
        )
        mesh.buffer(numpy.array([0.0, 0.0, 1.0, 1.0], dtype="f4"), "2f", "uv")

        # Ensure basic properties are correct
        self.assertEqual(mesh.name, "test")
        self.assertEqual(mesh.vertex_count, 2)
        self.assertEqual(mesh.mode, moderngl.LINES)

        # Ensure buffers are present
        self.assertIsInstance(mesh.get_buffer_by_name("position"), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name("normal"), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name("uv"), BufferInfo)
        self.assertEqual(mesh.get_buffer_by_name("something"), None)

        # Create a progam using a subset of the buffers
        prog = self.createProgram()
        vao = mesh.instance(prog)
        self.assertIsInstance(vao, moderngl.VertexArray)

        # Render directly with VAO and VertexArray instance
        mesh.render(prog)
        vao.render()

    def test_illegal_draw_mode(self):
        """Create vao with illegal draw mode"""
        with self.assertRaises(VAOError):
            VAO(mode=1337)

    def test_program_id_collision(self):
        """Reused numeric names must not select another program's VAO."""
        mesh = VAO("program_cache", mode=moderngl.POINTS)
        first_buffer = mesh.buffer(numpy.array([1, 2], dtype="f4"), "1f", "first")
        second_buffer = mesh.buffer(numpy.array([10, 20], dtype="f4"), "1f", "second")
        first = self.ctx.program(
            vertex_shader="""
                #version 330
                in float first;
                out float value;
                void main() { value = first * 2.0; }
            """,
            varyings=["value"],
        )
        second = self.ctx.program(
            vertex_shader="""
                #version 330
                in float second;
                out float value;
                void main() { value = second * 3.0; }
            """,
            varyings=["value"],
        )
        output = self.ctx.buffer(reserve=8)
        try:
            # Make numeric-name reuse deterministic without depending on the
            # driver's allocation policy. The linked programs and GPU work are real.
            with patch.object(moderngl.Program, "glo", new_callable=PropertyMock, return_value=1):
                first_vao = mesh.instance(first)
                self.assertIs(mesh.instance(first), first_vao)
                mesh.transform(first, output, vertices=2)
                numpy.testing.assert_array_equal(
                    numpy.frombuffer(output.read(), dtype="f4"), [2, 4]
                )

                mesh.transform(second, output, vertices=2)
                numpy.testing.assert_array_equal(
                    numpy.frombuffer(output.read(), dtype="f4"), [30, 60]
                )
                second_vao = mesh.instance(second)
                self.assertIsNot(second_vao, first_vao)
                self.assertIs(mesh.instance(second), second_vao)
            self.assertEqual(len(mesh.vaos), 2)
        finally:
            mesh.release(buffer=False)
            output.release()
            first.release()
            second.release()
        self.assertEqual(mesh.vaos, {})
        # Releasing the cached VAOs must honor buffer=False.
        self.assertEqual(first_buffer.read(), numpy.array([1, 2], dtype="f4").tobytes())
        self.assertEqual(second_buffer.read(), numpy.array([10, 20], dtype="f4").tobytes())
        first_buffer.release()
        second_buffer.release()

    def test_add_illegal_buffer(self):
        """Attempt to add illegal buffer"""
        vao = VAO()
        with self.assertRaises(VAOError):
            vao.buffer("stuff", "1f", "in_position")

    def test_normalized_types(self):
        """Ensure VAO wrapper can handle normalized types"""
        # prog = self.createProgram()
        mesh = VAO("test", mode=moderngl.LINES)
        mesh.buffer(
            numpy.array([0.0, 0.0, 0.0, 1.0, 1.0, 1.0], dtype="i4"), "3ni", "position"
        )
        mesh.buffer(
            numpy.array([0.0, 0.0, 1.0, 1.0, 0.0, 1.0], dtype="f4"), "3nf", "normal"
        )
        mesh.buffer(numpy.array([0.0, 0.0, 1.0, 1.0], dtype="f4"), "2f", "uv")

        # Uncomment in moderngl 5.6+
        # mesh.instance(prog)

    def test_divisors(self):
        """Test defining buffers with different divisor types"""
        mesh = VAO("test", mode=moderngl.LINES)
        mesh.buffer(
            numpy.array([0.0, 0.0, 0.0, 1.0, 1.0, 1.0], dtype="f4"), "3f/v", "position"
        )
        mesh.buffer(
            numpy.array([0.0, 0.0, 1.0, 1.0, 0.0, 1.0], dtype="f4"), "3f/r", "normal"
        )
        mesh.buffer(numpy.array([0.0, 0.0, 1.0, 1.0], dtype="f4"), "2f/i", "uv")

        buffer1 = mesh.get_buffer_by_name("position")
        buffer2 = mesh.get_buffer_by_name("normal")
        buffer3 = mesh.get_buffer_by_name("uv")

        attributes = ["position", "normal", "uv"]
        self.assertEqual(
            buffer1.content(attributes), (buffer1.buffer, "3f/v", "position")
        )
        self.assertEqual(
            buffer2.content(attributes), (buffer2.buffer, "3f/r", "normal")
        )
        self.assertEqual(buffer3.content(attributes), (buffer3.buffer, "2f/i", "uv"))
