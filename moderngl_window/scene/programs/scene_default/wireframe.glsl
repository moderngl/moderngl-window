#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;

uniform mat4 m_proj;
// Use separate model and camera matrix. This means we don't have
// to calculate modelview matrix in python every frame
uniform mat4 m_model;
uniform mat4 m_cam;

void main() {
    gl_Position = m_proj * m_cam * m_model * vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform vec4 color;

void main()
{
    fragColor = color;
}

#endif
