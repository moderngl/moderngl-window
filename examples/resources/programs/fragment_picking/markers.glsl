#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;
out vec2 uv;

out vec3 normal;

void main() {
    gl_Position = vec4(in_position, 1.0);
    normal = in_normal;
}

#elif defined GEOMETRY_SHADER

layout(points) in;
layout(points, max_vertices = 1) out;

uniform mat4 projection;
uniform mat4 modelview;

in vec3 normal[1];

void main() {
    mat3 normalMatrix = inverse(transpose(mat3(modelview)));
    vec3 normalTransformed = normalMatrix * normalize(normal[0]);
    vec4 positionTransformed = modelview * gl_in[0].gl_Position;

    if (dot(normalTransformed, -normalize(positionTransformed.xyz)) > 0.1) {
        gl_Position = projection * positionTransformed;
        EmitVertex();
        EndPrimitive();
    }
}

#elif defined FRAGMENT_SHADER

out vec4 out_color;
uniform vec4 color;

void main() {
    out_color = color;
}
#endif
