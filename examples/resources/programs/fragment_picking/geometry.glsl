#version 330

#if defined VERTEX_SHADER

uniform mat4 modelview;
uniform mat4 projection;

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

out vec2 uv;
out vec3 normal;

void main() {
    gl_Position = projection * modelview * vec4(in_position, 1.0);
    // mat3 normal_matrix = transpose(inverse(mat3(modelview)));
    // normal = normal_matrix * in_normal;
    normal = in_normal;
    uv = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

layout(location=0) out vec4 out_color;
layout(location=1) out vec4 out_normal;

in vec2 uv;
in vec3 normal;

uniform sampler2D texture0;

void main() {
    out_color = texture(texture0, uv);
    out_normal = vec4(normalize(normal), 0.0);
}
#endif
