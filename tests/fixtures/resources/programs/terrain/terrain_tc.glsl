#version 410

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
