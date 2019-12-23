#version 330

#if defined VERTEX_SHADER

in vec3 in_position;

uniform mat4 modelview;
uniform mat4 projection;

void main() {
    gl_Position = projection * modelview * vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 out_color;

void main() {
    out_color = vec4(1.0);
}
#endif
