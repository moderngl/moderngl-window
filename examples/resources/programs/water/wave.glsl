#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;

out vec2 uv0;

void main() {
    gl_Position = vec4(in_position, 1.0);
    uv0 = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
in vec2 uv0;

uniform sampler2D texture0;

void main() {
    float v = 0.25;
    ivec2 uv = ivec2(gl_FragCoord.xy);

    vec4 c1 = texelFetch(texture0, ivec2(uv + ivec2(-1, 1)), 0) * v;
    vec4 c2 = texelFetch(texture0, ivec2(uv + ivec2( 0, 1)), 0)  * v;
    vec4 c3 = texelFetch(texture0, ivec2(uv + ivec2( 1, 1)), 0)  * v;

    vec4 c4 = texelFetch(texture0, ivec2(uv + ivec2(-1, 0)), 0)  * v;
    vec4 c5 = texelFetch(texture0, ivec2(uv + ivec2( 0, 0)), 0) * 0.0;
    vec4 c6 = texelFetch(texture0, ivec2(uv + ivec2( 1, 0)), 0)  * v;

    vec4 c7 = texelFetch(texture0, ivec2(uv + ivec2(-1, -1)), 0)  * v;
    vec4 c8 = texelFetch(texture0, ivec2(uv + ivec2( 0, -1)), 0)  * v;
    vec4 c9 = texelFetch(texture0, ivec2(uv + ivec2( 1, -1)), 0)  * v;

    fragColor = (c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9) / 1.9;
}
#endif
