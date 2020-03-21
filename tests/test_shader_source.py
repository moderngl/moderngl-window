from unittest import TestCase
from moderngl_window.opengl import program


class ShaderSourceTestCase(TestCase):

    def test_no_version(self):
        """Missing #version statement should raise a shader error"""
        with self.assertRaises(program.ShaderError):
            program.ShaderSource(
                program.VERTEX_SHADER,
                "test.glsl",
                """
                in vec2 in_pos;
                out vec2 out_pos;
                void main() {
                    out_pos = in_pos;
                }
                """
            )

    def test_no_version_first_line(self):
        """A shader should always start have a #version statement on the first line"""
        with self.assertRaises(program.ShaderError):
            program.ShaderSource(
                program.VERTEX_SHADER,
                "test.glsl",
                """
                in vec2 in_pos;
                out vec2 out_pos;
                # version 330
                void main() {
                    out_pos = in_pos;
                }
                """
            )

    def test_version_strip(self):
        """Make sure we can start with blank lines before #version"""
        program.ShaderSource(
            program.VERTEX_SHADER,
            "test.glsl",
            """

            #version 330
            in vec2 in_pos;
            out vec2 out_pos;
            void main() {
                out_pos = in_pos;
            }
            """
        )

    def test_define(self):
        """inject a define value"""
        shader = program.ShaderSource(
            program.VERTEX_SHADER,
            "test.glsl",
            """
            #version 330
            in vec2 in_pos;
            out vec2 out_pos;
            #define NUM_THINGS 16
            #define SCALE = 1.0
            void main() {
                out_pos = in_pos * SCALE;
            }
            """,
            defines={'NUM_THINGS': '100', 'SCALE': '2.0'}
        )
        self.assertTrue("#define NUM_THINGS 100" in shader.source)
        self.assertTrue("#define SCALE 2.0" in shader.source)
