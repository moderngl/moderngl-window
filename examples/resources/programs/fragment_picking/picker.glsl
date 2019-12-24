#version 330
//
// Picks a point from the depth buffer and returns the world position
//

#if defined VERTEX_SHADER

in vec2 in_position;

uniform sampler2D position_texture;
uniform mat4 modelview;
uniform ivec2 texel_pos;

out vec3 out_position;

void main() {
    vec3 viewpos = texelFetch(position_texture, texel_pos, 0).rgb;
    out_position = (inverse(modelview) * vec4(viewpos, 1.0)).xyz;
}

#endif
