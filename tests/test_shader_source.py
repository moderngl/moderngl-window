from pathlib import Path
from unittest import TestCase
from moderngl_window.opengl import program
from moderngl_window import resources
from moderngl_window.meta import DataDescription

resources.register_dir((Path(__file__).parent / 'fixtures/resources').resolve())


class ShaderSourceTestCase(TestCase):
    maxDiff = None

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

    def test_define_compute(self):
        """Injecting defines in compute shader"""
        shader = program.ShaderSource(
            program.COMPUTE_SHADER,
            "compute.glsl",
            """
            #version 430
            #define TEST 0
            #define THING 0
            layout (local_size_x = 1, local_size_y = 1) in;
            layout (std430, binding = 1) buffer Input {
                float v1[4];
            };
            layout (std430, binding = 2) buffer Output {
                float v2[4];
            };
            uniform float mul;
            uniform vec4 add;
            void main() {
                v2[0] = v1[3] * mul + add.x;
                v2[1] = v1[2] * mul + add.y;
                v2[2] = v1[1] * mul + add.z;
                v2[3] = v1[0] * mul + add.w;
            }
            """,
            defines={'TEST': 12, 'THING': '23'},
        )
        self.assertTrue("#define TEST 12" in shader.source)
        self.assertTrue("#define THING 23" in shader.source)

    def test_out_attributes(self):
        """Ensure out attributes are proprely parsed"""
        shader = program.ShaderSource(
            program.VERTEX_SHADER,
            "test.glsl",
            """
            #version 330
            out vec2 out_pos;
            out vec2 out_vel;
            void main() {
                out_pos = vec2(1.0);
                out_vel = vec2(1.0);
            }
            """,
        )
        assert shader.find_out_attribs() == ['out_pos', 'out_vel']
        # With layout qualifiers
        shader = program.ShaderSource(
            program.VERTEX_SHADER,
            "test.glsl",
            """
            #version 330
            layout(location = 0) out vec2 out_pos;
            layout(location = 1) out vec2 out_vel;
            void main() {
                out_pos = vec2(1.0);
                out_vel = vec2(1.0);
            }
            """,
        )
        assert shader.find_out_attribs() == ['out_pos', 'out_vel']

    def test_include(self):
        """Test #include preprocessors (recursive)"""
        def load_source(path):
            return path, resources.data.load(DataDescription(path, kind='text'))

        path = 'programs/include_test.glsl'
        source = load_source(path)[1]
        source_vs = program.ShaderSource(program.VERTEX_SHADER, path, source, defines={'TEST': '100'})
        source_vs.handle_includes(load_source)

        self.assertEqual(source_vs.source, INCLUDE_RESULT)
        self.assertEqual(source_vs.source_list[0].name, 'programs/include_test.glsl')
        self.assertEqual(source_vs.source_list[0].id, 0)
        self.assertEqual(source_vs.source_list[1].name, 'programs/includes/blend_functions.glsl')
        self.assertEqual(source_vs.source_list[1].id, 1)
        self.assertEqual(source_vs.source_list[2].name, 'programs/includes/utils.glsl')
        self.assertEqual(source_vs.source_list[2].id, 2)
        self.assertEqual(source_vs.source_list[3].name, 'programs/includes/utils_1.glsl')
        self.assertEqual(source_vs.source_list[3].id, 3)
        self.assertEqual(source_vs.source_list[4].name, 'programs/includes/utils_2.glsl')
        self.assertEqual(source_vs.source_list[4].id, 4)

    def test_include_circular(self):
        """Ensure circular includes are detected"""
        def load_source(path):
            return path, resources.data.load(DataDescription(path, kind='text'))

        path = 'programs/include_test_circular.glsl'
        _, source = load_source(path)
        source = program.ShaderSource(program.VERTEX_SHADER, path, source)
        with self.assertRaises(program.ShaderError):
            source.handle_includes(load_source)


INCLUDE_RESULT = """#version 330
#define VERTEX_SHADER 1
#line 2

vec3 blendMultiply(vec3 base, vec3 blend) {
	return base * blend;
}

vec3 blendMultiply(vec3 base, vec3 blend, float opacity) {
	return (blendMultiply(base, blend) * opacity + base * (1.0 - opacity));
}

// Utils 1
#define TEST 100

// Utils 2
#define TEST 100



#define TEST 100

#if defined VERTEX_SHADER

in vec3 in_position;

void main() {
    gl_Position = vec4(in_position, 1.0);
}


#elif defined FRAGMENT_SHADER

out vec4 fragColor;

void main() {
    fragColor = vec4(1.0);
}

#endif"""
