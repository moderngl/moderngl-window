#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;

uniform mat4 m_proj;
uniform mat4 m_model;
uniform mat4 m_camera;

out vec2 uv;

void main() {
    gl_Position = m_proj * m_camera * m_model * vec4(in_position, 1);
    uv = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
in vec2 uv;

uniform sampler2DArray texture0;
uniform float num_layers;
uniform float time;

void main() {
    // Get the current and next texture layer
    float layer = floor(time);
    vec4 c1 = texture(texture0, vec3(uv, mod(layer, num_layers)));
    vec4 c2 = texture(texture0, vec3(uv, mod(layer + 1.0, num_layers)));

    // Interpolate between the two texture layers
    float t = mod(time, 1.0);
    fragColor = (c1 * (1.0 - t) + c2 * t) + vec4(0.25);
}
#endif
