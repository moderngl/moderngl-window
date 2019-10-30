#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;

uniform vec2 pos;

out vec2 uv0;

void main() {
    gl_Position = vec4(vec3(in_position.xy + pos.xy, 0.0), 1.0);
    uv0 = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

uniform sampler2D texture0;
const float FORCE = 2.5;

out vec4 fragColor;
in vec2 uv0;

void main() {
    float val = texture(texture0, uv0).r;
    fragColor = vec4(val, val, val, 0) * FORCE;
}
#endif
