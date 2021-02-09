#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_offset;

uniform mat4 m_proj;
uniform mat4 m_modelview;

void main() {
	gl_Position = m_proj * m_modelview * vec4(in_position + in_offset, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;

void main()
{
    fragColor = vec4(1.0);
}

#endif
