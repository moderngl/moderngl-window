#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;
out vec2 uv;

void main() {
    gl_Position = vec4(in_position, 1);
    uv = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
in vec2 uv;

void main() {
    vec3 col1 = vec3(30./255., 48./255., 73./255.) * uv.y;
    vec3 col2 = vec3(155./255., 169./255., 191./255.) * (1-0 - uv.y);
    fragColor = vec4(col1 + col2, 1.0);
}
#endif
