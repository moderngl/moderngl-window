#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;

// Per instance
in vec3 in_offset;

uniform mat4 m_proj;
uniform mat4 m_modelview;
uniform mat3 m_normal;

out vec3 normal;
out vec3 pos;

void main() {
    vec4 p = m_modelview * vec4(in_position + in_offset, 1.0);
    gl_Position = m_proj * p;
    normal = m_normal * in_normal;
    pos = p.xyz;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
const vec4 color = vec4(1.0);

in vec3 normal;
in vec3 pos;

void main()
{
    // Just use the camera as the only light source
    float l = dot(normalize(-pos), normalize(normal));
    // 25% ambient, 75% light
    fragColor = color * (0.25 + abs(l) * 0.75);
}

#endif
