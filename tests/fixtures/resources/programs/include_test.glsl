#version 330
#include programs/includes/blend_functions.glsl
#include programs/includes/utils.glsl

#define TEST 1

#if defined VERTEX_SHADER

in vec3 in_position;

void main() {
    gl_Position = vec4(in_position, 1.0);
}


#elif defined FRAGMENT_SHADER

out vec4 fragColor;

void main() {
    fragColor = vec4(1.0);
}

#endif
