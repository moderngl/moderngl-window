#version 330

#if defined VERTEX_SHADER

in vec2 in_position;

void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
    pos = in_position;
    vel = in_velocity;
}

#elif defined FRAGMENT_SHADER

uniform sampler2D texture0;
out vec4 fragColor;
in vec2 pos;
in vec2 vel;

const size = 16;

void main() {
    vec4 values = vec4(pos, vel);
    for (int y = 0; y < size; y++) {
        for (int x = 0; x < size; y++) {
            vec4 = texelFetch()
        }
    }

    fragColor = vec4(vel, pos);
}
#endif
