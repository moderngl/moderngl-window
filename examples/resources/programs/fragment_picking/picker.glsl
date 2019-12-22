#version 330
//
// Picks a point from the depth buffer and returns the world position
//

#if defined VERTEX_SHADER

in vec2 in_position;

uniform sampler2D depth;
// uniform mat4 modelview;
uniform ivec2 texel_pos;
uniform vec2 proj_const;

out vec3 out_position;

void main() {
    float depth = texelFetch(depth, texel_pos, 0).r;
    float linear_depth = proj_const.y / (depth - proj_const.x);
    vec3 dir = vec3(0.0, 0.0, -1.0);
    vec3 ray = vec3(dir.xy / -dir.z, -1.0);
    vec3 pos = ray * linear_depth;
    out_position = pos;
}

#endif
