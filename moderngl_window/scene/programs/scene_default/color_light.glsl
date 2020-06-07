#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;

uniform mat4 m_proj;
// Use separate model and camera matrix. This means we don't have
// to calculate modelview matrix in python every frame
uniform mat4 m_model;
uniform mat4 m_cam;

out vec3 normal;
out vec3 pos;

void main() {
    mat4 mv = m_cam * m_model;
    vec4 p = mv * vec4(in_position, 1.0);
    gl_Position = m_proj * p;
    // Calculating the normal matrix in the vertex shader
    // means we don't have to do this expensive calculation in python
    mat3 m_normal = transpose(inverse(mat3(mv)));
    normal = m_normal * in_normal;
    // Pass to position to fragment shader so we get an interpolated
    // position over the entire triangle for per pixel lighting
    pos = p.xyz;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform vec4 color;

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
