#version 330

#if defined VERTEX_SHADER

uniform mat4 mvp;

in vec3 in_position;
in vec3 in_normal;

out vec3 pos;
out vec3 normal;

void main() {
    gl_Position = mvp * vec4(in_position, 1.0);;
    pos = in_position;
    normal = in_normal;
}

#elif defined FRAGMENT_SHADER

uniform mat4 m_camera;

in vec3 pos;
in vec3 normal;

layout(location=0) out float g_view_z;
layout(location=1) out vec3 g_normal;

void main() {
    // Rotate into view space, and record the z component.
    g_view_z = -(m_camera * vec4(pos, 1.0)).z;
    g_normal = normalize(normal);
}

#endif
