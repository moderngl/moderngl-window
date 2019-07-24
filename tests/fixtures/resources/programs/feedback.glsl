#version 330

#if defined VERTEX_SHADER

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_velocity;

out vec3 out_position;
out vec3 out_velocity;

uniform float timedelta;
uniform vec3 gravity_pos;
uniform float gravity_force;

void main() {
    // direction towards the gravity point
    vec3 dir = normalize(gravity_pos - in_position) * gravity_force;
    float l = length(gravity_pos - in_position) / 10.0;
    // Add gravity to velocity
    vec3 vel = in_velocity - (dir / l * timedelta);
    out_velocity = vel;
	out_position = in_position - (vel * timedelta);
}

#endif
