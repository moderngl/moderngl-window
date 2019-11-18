#version 330

#if defined VERTEX_SHADER

in vec3 in_position;

void main() {
	gl_Position = vec4(in_position, 1.0);
}

#elif defined GEOMETRY_SHADER

layout (lines) in;
layout (triangle_strip, max_vertices = 4) out;

uniform mat4 m_proj;
uniform mat4 m_model;
uniform mat4 m_cam;

void main() {
    const float size = 0.03;
    vec3 a = gl_in[0].gl_Position.xyz;
    vec3 b = gl_in[1].gl_Position.xyz;

    vec3 up = vec3(0.0, 1.0, 0.0) * size;
    vec3 right = vec3(1.0, 0.0, 0.0) * size;

    mat4 mvp = m_proj * m_cam * m_model;

    gl_Position = mvp * vec4(a - up, 1.0);
    EmitVertex();

    gl_Position = mvp * vec4(a + up, 1.0);
    EmitVertex();

    gl_Position = mvp * vec4(b - up, 1.0);
    EmitVertex();

    gl_Position = mvp * vec4(b + up, 1.0);
    EmitVertex();

    EndPrimitive();
}

#elif defined FRAGMENT_SHADER

out vec4 outColor;
uniform vec4 color;

void main() {
    outColor = color;
}

#endif
