#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

uniform mat4 m_model;
uniform mat4 m_camera;
uniform mat4 m_proj;

out vec3 pos;
out vec3 normal;
out vec2 uv;

void main() {
    mat4 m_view = m_camera * m_model;
    vec4 p = m_view * vec4(in_position, 1.0);
    gl_Position =  m_proj * p;
    mat3 m_normal = inverse(transpose(mat3(m_view)));
    normal = m_normal * normalize(in_normal);
    uv = in_texcoord_0;
    pos = p.xyz;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;

uniform sampler2D texture0;

in vec3 pos;
in vec3 normal;
in vec2 uv;

void main() {
    float l = dot(normalize(-pos), normalize(normal));
    fragColor = texture(texture0, uv) * (0.25 + abs(l) * 0.75);
}
#endif
