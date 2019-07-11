#version 330

#if defined VERTEX_SHADER

in vec3 in_position;

uniform mat4 m_proj;
uniform mat4 m_model;
uniform mat4 m_cam;

uniform vec3 bb_min;
uniform vec3 bb_max;

void main() {
    vec3 size = bb_max - bb_min;
	gl_Position = m_proj * m_cam * m_model * vec4((in_position * size) + bb_min + size / 2.0, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform vec3 color;

void main()
{
    fragColor = vec4(color, 1.0);
}

#endif
