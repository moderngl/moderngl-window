#version 430

layout (local_size_x = 16, local_size_y = 16) in;
// match the input texture format!
layout(rgba8, location=0) writeonly uniform image2D destTex;
uniform float time;

void main() {
    // texel coordinate we are writing to
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    // Calculate 1.0 - distance from the center in each work group
    float local = 1.0 - length(vec2(ivec2(gl_LocalInvocationID.xy) - 8) / 8.0);
    // Wave covering the screen diagonally
    float global = sin(float(gl_WorkGroupID.x + gl_WorkGroupID.y) * 0.1 + time) / 2.0 + 0.5;
    imageStore(
        destTex,
        texelPos,
        vec4(
            local,
            global,
            0.0,
            1.0
        )
    );
}
