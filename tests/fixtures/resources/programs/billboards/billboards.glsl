#version 330

#if defined VERTEX_SHADER

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_velocity;

out vec3 vert_color;

void main() {
    vert_color = vec3(length(in_velocity) / 15.0, 0.25, 0.25);
	gl_Position = vec4(in_position, 1.0);
}

#elif defined GEOMETRY_SHADER

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

uniform mat4 m_proj;
uniform mat4 m_mv;

in vec3 vert_color[1];
out vec2 uv;
out vec3 geo_color;

void main() {
    //float size = gl_in[0].gl_PointSize;
    //color = size;
    const float size = 2.0;
    vec3 pos = gl_in[0].gl_Position.xyz;
    vec3 right = vec3(m_mv[0][0], m_mv[1][0], m_mv[2][0]);
    vec3 up = vec3(m_mv[0][1], m_mv[1][1], m_mv[2][1]);

    uv = vec2(1.0, 1.0);
    geo_color = vert_color[0];
    gl_Position = m_proj * m_mv * vec4(pos + (right + up) * size, 1.0);
    EmitVertex();

    uv = vec2(0.0, 1.0);
    geo_color = vert_color[0];
    gl_Position = m_proj * m_mv * vec4(pos + (-right + up) * size, 1.0);
    EmitVertex();

    uv = vec2(1.0, 0.0);
    geo_color = vert_color[0];
    gl_Position = m_proj * m_mv * vec4(pos + (right - up) * size, 1.0);
    EmitVertex();

    uv = vec2(0.0, 0.0);
    geo_color = vert_color[0];
    gl_Position = m_proj * m_mv * vec4(pos + (-right - up) * size, 1.0);
    EmitVertex();

    EndPrimitive();
}

#elif defined FRAGMENT_SHADER

out vec4 outColor;
in vec2 uv;
in vec3 geo_color;

uniform sampler2D texture0;

void main() {
    outColor = texture(texture0, uv) * vec4(geo_color, 1.0);
}

#endif
