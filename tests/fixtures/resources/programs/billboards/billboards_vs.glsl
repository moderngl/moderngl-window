#version 330

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_velocity;

out vec3 vert_color;

void main() {
    vert_color = vec3(length(in_velocity) / 15.0, 0.25, 0.25);
	gl_Position = vec4(in_position, 1.0);
}
