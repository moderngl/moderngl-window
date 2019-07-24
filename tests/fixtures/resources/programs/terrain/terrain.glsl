#version 410

#if defined VERTEX_SHADER

in vec3 in_position;
out vec3 v_position;

void main() {
    v_position = in_position.xyz;
}

#elif defined TESS_CONTROL_SHADER

layout(vertices = 3) out;

in vec3 v_position[];
out vec3 tc_position[];

uniform float TessLevelInner;
uniform float TessLevelOuter;

void main() {
    tc_position[gl_InvocationID] = v_position[gl_InvocationID];
    if (gl_InvocationID == 0) {
        // Resolution inside the triangle
        gl_TessLevelInner[0] = TessLevelInner;
        
        // How many segments each edge of the triagle should be split into
        gl_TessLevelOuter[0] = TessLevelOuter;
        gl_TessLevelOuter[1] = TessLevelOuter;
        gl_TessLevelOuter[2] = TessLevelOuter;
    }
}

#elif defined TESS_EVALUATION_SHADER

layout(triangles, equal_spacing, ccw) in;

in vec3 tc_position[];
out vec2 ts_uv;

uniform mat4 m_mv;
uniform mat4 m_proj;
uniform sampler2D heightmap;

void main() {
    // gl_TessCoord is barycentric coordinates inside the triangle representing the new vertex positions
    // We multiply that with the three vertex position to get the new vertex position
    vec3 p0 = gl_TessCoord.x * tc_position[0];
    vec3 p1 = gl_TessCoord.y * tc_position[1];
    vec3 p2 = gl_TessCoord.z * tc_position[2];

    // Add them together to get the actual world posision
    vec3 pos = p0 + p1 + p2;

    // Read the height from the heightmap
    vec2 uv = vec2(0.5, 0.5) + vec2(pos.xz) / 400.0;
    float height = texture(heightmap, uv).r;

    // Emit new vertex
    gl_Position = m_proj * m_mv * vec4(vec3(pos.x, height * 25.0, pos.z), 1.0);
    ts_uv = uv;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
in vec2 ts_uv;
uniform sampler2D heightmap;

void main() {
    float color = texture(heightmap, ts_uv).r;
    fragColor = vec4(color);
}

#endif
