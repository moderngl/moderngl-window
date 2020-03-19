#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;
uniform mat4 projection;
uniform vec2 position;
uniform sampler2DArray texture0;
out vec2 uv0;

void main() {
    gl_Position = projection * vec4(in_position.xy * textureSize(texture0, 0).xy + position, 0, 1);
    uv0 = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform sampler2DArray texture0;
uniform int layer_id;
in vec2 uv0;

void main() {
    fragColor = texture(texture0, vec3(uv0, layer_id));
}
#endif
