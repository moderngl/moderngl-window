#version 410

in vec3 in_position;
out vec3 v_position;

void main() {
    v_position = in_position.xyz;
}
