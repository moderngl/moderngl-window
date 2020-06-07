#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;
in vec3 in_color0;

uniform mat4 m_proj;
uniform mat4 m_model;
uniform mat4 m_cam;

out vec3 color;
out vec2 uv;

void main() {
    gl_Position = m_proj * m_cam * m_model * vec4(in_position, 1.0);
    color = in_color0;
    uv = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

uniform sampler2D texture0;
out vec4 fragColor;
in vec3 color;
in vec2 uv;

void main()
{
    fragColor = vec4(texture(texture0, uv).rgb * color, 1.0);
}

#endif
