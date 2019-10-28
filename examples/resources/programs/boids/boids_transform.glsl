#version 330

#if defined VERTEX_SHADER

layout (location = 0) in vec2 in_position;
layout (location = 1) in vec2 in_velocity;

out vec2 out_position;
out vec2 out_velocity;

uniform float timedelta;
uniform sampler2D data;
uniform int num_boids;
uniform int tex_width;

const float MAX_SPEED = 0.1;

ivec2 texelPos(int i) {
    return ivec2(i % tex_width, i / num_boids);
}

void read_boid(out vec2 pos, out vec2 vel, int i) {
    pos = texelFetch(data, texelPos(i), 0).rg;
    vel = texelFetch(data, texelPos(i + 1), 0).rg;
}

void main() {
    vec2 tmp_pos = vec2(0.0);
    vec2 tmp_vel = vec2(0.0);

    vec2 boid_co = vec2(0.0);
    vec2 boid_se = vec2(0.0);
    vec2 boid_vel = vec2(0.0);

    int count = 0;
    for (int i = 0; i < num_boids; i++) {
        if (i == gl_VertexID) {
            continue;
        }
        read_boid(tmp_pos, tmp_vel, i);
        float dist = distance(in_position, tmp_pos);
        if (dist < 0.1) {
            // alignment
            boid_vel += tmp_vel;

            // separation
            boid_se += tmp_pos;

            // cohesion
            boid_co += tmp_pos;

            count++;
        }
    }
    if (count > 0) {
        boid_vel /= count;
        boid_co /= count;
        boid_se /= count;

        boid_vel += in_position - boid_co;
//        boid_vel += in_position + boid_se;

        float speed = length(boid_vel);
        if (speed > MAX_SPEED) {
            boid_vel *= MAX_SPEED / speed;
        }
    }
    // handle framebuffer bounds
    vec2 pos = in_position + (boid_vel * timedelta);
    vec2 vel = in_velocity + boid_vel;

    // float len = 1.0; // max(length(boid_vel), 0.1);
    float dist_x_pos = 2.5 - pos.x;
    float dist_x_neg = abs(-2.5 - pos.x);
    float dist_y_pos = 1.0 - pos.y;
    float dist_y_neg = abs(-1.0 - pos.y);

    if (dist_x_pos < 0.1) {
        vel += vec2(-1.0, 0.0);
    }
    if (dist_x_neg < 0.1) {
        vel += vec2(1.0, 0.0);
    }
    if (dist_y_pos < 0.1) {
        vel += vec2(0.0, -1.0);
    }
    if (dist_y_neg < 0.1) {
        vel += vec2(0.0, 1.0);
    }

	out_position = pos;
    out_velocity = vel;
}

#endif
