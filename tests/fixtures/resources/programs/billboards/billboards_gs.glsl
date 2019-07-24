#version 330

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
