#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
uniform mat4 projection;
uniform mat4 modelview;
out vec2 uv;

void main() {
    gl_Position = projection * modelview * vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 out_color;
uniform vec4 color;

void main() {
    out_color = color;
}
#endif
