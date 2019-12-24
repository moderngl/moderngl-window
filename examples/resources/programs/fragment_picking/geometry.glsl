#version 330

#if defined VERTEX_SHADER

uniform mat4 modelview;
uniform mat4 projection;

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

out vec2 uv;
out vec3 normal;
out vec3 pos;

void main() {
    vec4 p = modelview * vec4(in_position, 1.0);
    gl_Position = projection * p;
    // // We don't need to rotate normal matrix in this situation
    // mat3 normal_matrix = transpose(inverse(mat3(modelview)));
    // normal = normal_matrix * in_normal;
    normal = in_normal;
    uv = in_texcoord_0;
    pos = p.xyz;
}

#elif defined FRAGMENT_SHADER

layout(location=0) out vec4 out_color;
layout(location=1) out vec4 out_normal;
layout(location=2) out vec4 out_position;

in vec2 uv;
in vec3 normal;
in vec3 pos;

uniform sampler2D texture0;

void main() {
    out_color = texture(texture0, uv);
    out_normal = vec4(normalize(normal), 0.0);
    out_position = vec4(pos, 0.0);
}
#endif
