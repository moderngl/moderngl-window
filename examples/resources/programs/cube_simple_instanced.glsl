#version 330

#if defined VERTEX_SHADER

// Model geometry
in vec3 in_position;
in vec3 in_normal;

// Per instance data
in vec3 in_offset;
in vec3 in_color;

uniform mat4 m_model;
uniform mat4 m_camera;
uniform mat4 m_proj;
uniform float time;

out vec3 pos;
out vec3 normal;
out vec3 color;

void main() {
    mat4 m_view = m_camera * m_model;
    vec4 p = m_view * vec4(in_position + in_offset + vec3(0.0, sin(gl_InstanceID + time) * 2.0, 0.0), 1.0);
    gl_Position =  m_proj * p;
    mat3 m_normal = inverse(transpose(mat3(m_view)));
    normal = m_normal * normalize(in_normal);
    pos = p.xyz;
    color = in_color;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;

in vec3 pos;
in vec3 normal;
in vec3 color;

void main() {
    float l = dot(normalize(-pos), normalize(normal));
    fragColor = vec4(color * (0.25 + abs(l) * 0.75), 1.0);
}
#endif
