#version 330

#if defined VERTEX_SHADER

in vec3 in_position;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = projection * model * view * vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 outColor;

void main() {
    outColor = vec4(1.0);
}

#endif
