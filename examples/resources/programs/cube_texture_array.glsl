#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;

uniform mat4 m_proj;
uniform mat4 m_model;
uniform mat4 m_camera;

uniform float layer;

out vec3 uv0;

void main() {
    gl_Position = m_proj * m_camera * m_model * vec4(in_position, 1);
    uv0 = vec3(in_texcoord_0, layer);
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform sampler2DArray texture0;
in vec3 uv0;

void main() {
    fragColor = texture(texture0, uv0) + vec4(0.25);
}
#endif
