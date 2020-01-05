#version 430
layout (local_size_x = 1, local_size_y = 1) in;
layout (std430, binding = 1) buffer Input {
    float v1[4];
};
layout (std430, binding = 2) buffer Output {
    float v2[4];
};
uniform float mul;
uniform vec4 add;
void main() {
    v2[0] = v1[3] * mul + add.x;
    v2[1] = v1[2] * mul + add.y;
    v2[2] = v1[1] * mul + add.z;
    v2[3] = v1[0] * mul + add.w;
}