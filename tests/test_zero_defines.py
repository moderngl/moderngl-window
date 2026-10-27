"""Zero-valued shader options must override source defaults."""

import pytest
from headless import HeadlessTestCase

from moderngl_window.meta import ProgramDescription
from moderngl_window.opengl.program import VERTEX_SHADER, ProgramShaders, ShaderSource


@pytest.mark.parametrize("root", [True, False])
@pytest.mark.parametrize(
    "value, expected", [(0, "0"), (0.0, "0.0"), ("", ""), ("0", "0"), (2, "2"), (None, "16")]
)
def test_define_values(root, value, expected):
    shader = ShaderSource(
        VERTEX_SHADER,
        "test.glsl",
        "#version 330\n#define COUNT 16\n#define UNCHANGED 7\n",
        defines={"COUNT": value},
        root=root,
    )
    assert f"#define COUNT {expected}" in shader.lines
    assert "#define UNCHANGED 7" in shader.lines
    assert shader.lines[0] == "#version 330"


class ZeroDefineProgramTestCase(HeadlessTestCase):
    def test_numeric_zero_define(self):
        shaders = ProgramShaders.from_separate(
            ProgramDescription(defines={"COUNT": 0}),
            """#version 330
#define COUNT 16
#if COUNT != 0
#error Numeric zero override was ignored
#endif
void main() { gl_Position = vec4(0.0); }
""",
            fragment_source="""#version 330
out vec4 color;
void main() { color = vec4(1.0); }
""",
        )
        compiled = shaders.create()
        compiled.release()
