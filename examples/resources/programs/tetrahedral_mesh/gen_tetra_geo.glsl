#version 330

layout (lines_adjacency) in;
layout (triangle_strip, max_vertices = 12) out;

uniform mat4 m_cam;
uniform mat4 m_proj;

uniform sampler2D alive_texture;
uniform float threshold;


vec3 calc_normal(vec3 a, vec3 b, vec3 c) {
    return normalize(cross(c - a, b - a));
}

out vec3 pos;
out vec3 normal;

const int TEX_WIDTH = 8192;

#define EMIT_V(POS, NORMAL) \
	normal = NORMAL; \
    pos = POS.xyz; \
	gl_Position = POS; \
	EmitVertex()


void main() {
    // Check if the tehtra is alive
    ivec2 uv = ivec2(gl_PrimitiveIDIn % TEX_WIDTH, gl_PrimitiveIDIn / TEX_WIDTH);
    float value = texelFetch(alive_texture, uv, 0).a;

    if (value > 0.9) {
        vec3 v1 = gl_in[0].gl_Position.xyz;
        vec3 v2 = gl_in[1].gl_Position.xyz;
        vec3 v3 = gl_in[2].gl_Position.xyz;
        vec3 v4 = gl_in[3].gl_Position.xyz;

        mat4 mvp = m_proj * m_cam;
        // vertex positions
        vec4 p1 = mvp * vec4(v1, 1.0);
        vec4 p2 = mvp * vec4(v2, 1.0);
        vec4 p3 = mvp * vec4(v3, 1.0);
        vec4 p4 = mvp * vec4(v4, 1.0);
        // normals
        mat3 m_normal = transpose(inverse(mat3(m_cam))); 
        vec3 n1 = m_normal * calc_normal(v1, v3, v2);
        vec3 n2 = m_normal * calc_normal(v4, v1, v2);
        vec3 n3 = m_normal * calc_normal(v4, v2, v3);
        vec3 n4 = m_normal * calc_normal(v1, v4, v3);

        // Bottom [1, 3, 2]
        EMIT_V(p1, n1);
        EMIT_V(p3, n1);
        EMIT_V(p2, n1);
        EndPrimitive();

        // Front [4, 1, 2]
        EMIT_V(p4, n2);
        EMIT_V(p1, n2);
        EMIT_V(p2, n2);
        EndPrimitive();

        // Back [4, 2, 3]
        EMIT_V(p4, n3);
        EMIT_V(p2, n3);
        EMIT_V(p3, n3);
        EndPrimitive();

        // Left [1, 4, 3]
        EMIT_V(p1, n4);
        EMIT_V(p4, n4);
        EMIT_V(p3, n4);

        EndPrimitive();
    }
}
