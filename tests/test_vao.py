import moderngl
import numpy

from headless import HeadlessTestCase
from moderngl_window.opengl.vao import VAO, BufferInfo, VAOError


class VaoTestCase(HeadlessTestCase):

    def test_create(self):
        mesh = VAO("test", mode=moderngl.LINES)
        mesh.buffer(numpy.array([0.0, 0.0, 0.0, 1.0, 1.0, 1.0], dtype='f4'), '3f', 'position')
        mesh.buffer(numpy.array([0.0, 0.0, 1.0, 1.0, 0.0, 1.0], dtype='f4'), '3f', 'normal')
        mesh.buffer(numpy.array([0.0, 0.0, 1.0, 1.0], dtype='f4'), '2f', 'uv')

        # Ensure basic properties are correct
        self.assertEqual(mesh.name, "test")
        self.assertEqual(mesh.vertex_count, 2)
        self.assertEqual(mesh.mode, moderngl.LINES)

        # Ensure buffers are present
        self.assertIsInstance(mesh.get_buffer_by_name('position'), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name('normal'), BufferInfo)
        self.assertIsInstance(mesh.get_buffer_by_name('uv'), BufferInfo)
        self.assertEqual(mesh.get_buffer_by_name('something'), None)

        # Create a progam using a subset of the buffers
        prog = self.ctx.program(
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
            vao.buffer("stuff", '1f', 'in_position')
