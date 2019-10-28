#version 330

#if defined VERTEX_SHADER

layout (location = 0) in vec2 in_position;
layout (location = 1) in vec2 in_velocity;

// out vec3 vert_velocity;

void main() {
	gl_Position = vec4(in_position, 1.0, 1.0);
    // vert_velocity = vec3(in_velocity, 0.0);
}

#elif defined GEOMETRY_SHADER

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

uniform mat4 m_proj;

in vec3 vert_velocity[1];

void main() {
    const float size = 0.003;
    vec3 pos = gl_in[0].gl_Position.xyz;
    // vec3 up = normalize(vert_velocity[0]) * size;
    // vec3 right = cross(up, vec3(1.0, 0.0, 0.0)) * size;
    vec3 up = vec3(0.0, 1.0, 0.0) * size;
    vec3 right = vec3(1.0, 0.0, 0.0) * size;

    gl_Position = m_proj * vec4(pos + (right + up), 1.0);
    EmitVertex();

    gl_Position = m_proj * vec4(pos + (-right + up), 1.0);
    EmitVertex();

    gl_Position = m_proj * vec4(pos + (right - up), 1.0);
    EmitVertex();

    gl_Position = m_proj * vec4(pos + (-right - up), 1.0);
    EmitVertex();

    EndPrimitive();
}

#elif defined FRAGMENT_SHADER

out vec4 outColor;

void main() {
    outColor = vec4(1.0);
}

#endif
