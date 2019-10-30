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
uniform sampler2D texture0;
in vec2 uv0;

void main() {
    vec4 color = texture(texture0, uv0);
    vec4 c1 = texelFetch(texture0, ivec2(gl_FragCoord.xy + ivec2(1, 1)), 0);
    vec4 c2 = texelFetch(texture0, ivec2(gl_FragCoord.xy + ivec2(-1, 1)), 0);
    vec4 c3 = texelFetch(texture0, ivec2(gl_FragCoord.xy + ivec2(1, -1)), 0);
    vec4 c4 = texelFetch(texture0, ivec2(gl_FragCoord.xy + ivec2(-1, -1)), 0);
    fragColor = (c1 + c2 + c3 + c4) / 4.0;
}
#endif
