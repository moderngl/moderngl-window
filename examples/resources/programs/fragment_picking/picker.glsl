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
    if (viewpos.z == 0.0) {
        // A 0.0 z value means we missed the mesh. Just write out 0.0 as the result
        out_position = vec3(0.0);
    } else {
        // Reverse translations and rotations aligning the point with the original mesh
        out_position = (inverse(modelview) * vec4(viewpos, 1.0)).xyz;
    }
}

#endif
