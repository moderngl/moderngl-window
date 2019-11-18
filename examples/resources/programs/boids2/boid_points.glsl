#version 330

#if defined VERTEX_SHADER

in vec2 in_position;
in vec2 in_velocity;

out vec2 pos;
out vec2 vel;

void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
    pos = in_position;
    vel = in_velocity;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;

in vec2 pos;
in vec2 vel;

void main() {
    fragColor = vec4(vel, pos);
}
#endif
