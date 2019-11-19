#version 330

uniform vec3 color;

out vec4 fragColor;

in vec3 pos;
in vec3 normal;

void main() {
    float l = dot(normalize(-pos), normalize(normal));
    fragColor = vec4(color, 1.0) * (l / 3 + 0.66);
}
