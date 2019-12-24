#version 330
//
// Picks a point from the depth buffer and returns the world position
//

#if defined VERTEX_SHADER

in vec2 in_position;

uniform sampler2D depth_texture;
uniform mat4 modelview;
uniform ivec2 texel_pos;
uniform vec2 proj_const;
uniform float aspect_ratio;

out vec3 out_position;

void main() {
    float depth = texelFetch(depth_texture, texel_pos, 0).r;
    float linear_depth = proj_const.y / (depth - proj_const.x);
    vec2 pos = texel_pos / textureSize(depth_texture, 0) * vec2(2.0) - vec2(1.0);
    vec3 dir = vec3(pos.x, pos.y, -1.0);
    vec3 ray = vec3(dir.xy / -dir.z, -1.0);
    vec3 viewPos = ray * linear_depth;
    // out_position = (inverse(modelview) * vec4(viewPos, 1.0)).xyz;
    out_position = viewPos;
}

#endif
