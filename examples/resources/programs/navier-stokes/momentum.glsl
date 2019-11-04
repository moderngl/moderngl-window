#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;
out vec2 uv0;

void main() {
    gl_Position = vec4(in_position, 1);
    uv0 = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

out float fragColor;
in vec2 uv0;

uniform sampler2D momentum_texture;
uniform sampler2D pressure_texture;
uniform sampler2D walls_texture;

const ivec2 kpos[9] = ivec2[9](
    ivec2(-1,  1),  ivec2(0,  1),  ivec2(1,  1),
    ivec2(-1,  0),  ivec2(0,  0),  ivec2(1,  0),
    ivec2(-1, -1),  ivec2(0, -1),  ivec2(1, -1)
);

const float diff_kernel[9] = float[9](
    .025,  .1, .025,
      .1,  .5,   .1,
    .025,  .1, .025
);

const float con_kernel[9] = float[9](
      0.0, .25,   0.0,
     .25,  -1.0, .25,
      0.0, .25,   0.0
);

float diffusion(ivec2 uv, sampler2D source) {
    float value = 0;
    for (int i = 0; i < 9; i++) {
        value += texelFetch(source, uv + kpos[i], 0).r * diff_kernel[i];
    }
    return value;
}

const float viscosity = .018;
const float rho = 1.06;  // Density

float convection(ivec2 uv, sampler2D source) {
    float value = 0;
    for (int i = 0; i < 9; i++) {
        value += texelFetch(source, uv + kpos[i], 0).r * con_kernel[i];
    }
    return value;
}
const float external_flow = .35;
void main() {
    ivec2 uv = ivec2(gl_FragCoord.xy);

    float momentum = texelFetch(momentum_texture, uv, 0).r;
    float wall = texelFetch(walls_texture, uv, 0).r;
    
    float diff_momentum = diffusion(uv, momentum_texture);
    float con_momentum = convection(uv, momentum_texture);
    float con_pressure = convection(uv, pressure_texture);

    if (wall > 0) {
        fragColor = -external_flow;
    } else {
        fragColor = (diff_momentum - 
                    viscosity * momentum *
                    con_momentum +
                    con_pressure * rho); // * .994;
    }
}
#endif
