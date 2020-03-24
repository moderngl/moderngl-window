#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;
out vec2 uv0;

void main() {
    gl_Position = vec4(in_position, 1);
    uv0 = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform sampler2D texture0;
uniform sampler2D texture1;
in vec2 uv0;

#include programs/utils/library.glsl

void main() {
    vec4 c1 = texture(texture0, uv0);
    vec4 c2 = texture(texture1, uv0);

    if (uv0.x > 0.5) {
        if (uv0.y > 0.5) {
            fragColor = vec4(blendGlow(c1.rgb, c2.rgb), 1.0);
        }
        else {
            fragColor = vec4(blendColorBurn(c1.rgb, c2.rgb), 1.0);
        }
    }
    else {
        if (uv0.y > 0.5) {
            fragColor = vec4(blendNegation(c1.rgb, c2.rgb), 1.0);
        }
        else {
            fragColor = vec4(blendReflect(c1.rgb, c2.rgb), 1.0);
        }
    }
}
#endif
