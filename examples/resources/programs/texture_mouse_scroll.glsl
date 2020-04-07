#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;
out vec2 uv0;

void main() {
    gl_Position = vec4(in_position, 1);
    uv0 = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

uniform sampler2D texture0;
uniform vec2 offset;

out vec4 fragColor;
in vec2 uv0;

void main() {
    fragColor = texture(texture0, uv0 + offset);
}
#endif
