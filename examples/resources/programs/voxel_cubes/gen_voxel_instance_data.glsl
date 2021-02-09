#version 330

#if defined VERTEX_SHADER

uniform ivec3 voxel_size;

void main() {
    int x = gl_VertexID % voxel_size.x;
    int y = (gl_VertexID / voxel_size.y) % voxel_size.y;
    int z = gl_VertexID / (voxel_size.x * voxel_size.y);

    gl_Position = vec4(float(x), float(y), float(z), 0.0);
}

#elif defined GEOMETRY_SHADER

layout(points) in;
layout(points, max_vertices = 1) out;

uniform sampler2D lookup;
uniform ivec3 voxel_size;

out vec3 pos;

float lookup_3d(ivec3 p) {
    int x = (p.z * voxel_size.x) % 1000 + p.x % voxel_size.x;
    int y = (p.z / 10) * voxel_size.x + p.y;
    return texelFetch(lookup, ivec2(x, y), 0).r;
}

void main() {
    ivec3 p = ivec3(gl_in[0].gl_Position.xyz);
    float alive = lookup_3d(p);

    // Read all the neighbor cubes
    int neighbours = 0;
    if(lookup_3d(p + ivec3(0, 1, 0)) > 0) neighbours++;
    if(lookup_3d(p + ivec3(0, -1, 0)) > 0) neighbours++;
    if(lookup_3d(p + ivec3(-1, 0, 0)) > 0) neighbours++;
    if(lookup_3d(p + ivec3(1, 0, 0)) > 0) neighbours++;
    if(lookup_3d(p + ivec3(0, 0, 1)) > 0) neighbours++;
    if(lookup_3d(p + ivec3(0, 0, -1)) > 0) neighbours++;

    if (alive > 0) {
        // If we're at the voxel edge we should always render the cube
        if (p.x == 0 || p.x == 99) neighbours = 0;
        if (p.y == 0 || p.y == 99) neighbours = 0;
        if (p.z == 0 || p.z == 99) neighbours = 0;

        if (neighbours < 6) {
            pos = gl_in[0].gl_Position.xyz;
            EmitVertex();
        }
    }
}

#endif
