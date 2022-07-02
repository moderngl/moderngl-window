#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;

uniform mat4 mvp;

out vec3 pos;
out vec3 normal;

void main() {
    gl_Position = mvp * vec4(in_position, 1.0);
    pos = in_position;
    normal = in_normal;
}

#elif defined FRAGMENT_SHADER

in vec3 pos;
in vec3 normal;

out vec4 fragColor;

void main() {
    float l = dot(vec3(0.0, 1.0, 0.0), normalize(normal));
    fragColor = vec4(0.5, 0.5, 0.5, 1.0) * (0.25 + abs(l) * 0.75);
}

#endif
