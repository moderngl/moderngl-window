#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;

uniform mat4 m_proj;
uniform vec2 pos;

out vec2 uv0;

void main() {
    gl_Position = m_proj * vec4(vec3(in_position.xy + pos.xy, 0.0), 1.0);
    uv0 = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

// uniform sampler2D texture0;
uniform float write_value;
uniform float force;

out float fragColor;
in vec2 uv0;


void main() {
    // float val = texture(texture0, uv0).r;
    // if (val > 0.99) {
    //     fragColor = write_value;
    // }
    // else {
    //     discard;
    // }
    vec2 center = uv0 - vec2(0.5);
    float c = step(0.0, 0.5 - length(center));
    if (c > 0.99) fragColor = write_value * force;
    else discard;
}
#endif
