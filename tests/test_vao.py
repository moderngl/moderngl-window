import moderngl
import numpy

from headless import HeadlessTestCase
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
