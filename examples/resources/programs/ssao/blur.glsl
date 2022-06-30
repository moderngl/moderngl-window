#version 330 core

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;

out vec2 texcoord;

void main() {
    gl_Position = vec4(in_position, 1.0);
    texcoord = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

uniform sampler2D input_texture;

in vec2 texcoord;

layout(location=0) out float blurred_texture;

void main() {
    vec2 texel_size = 1.0 / vec2(textureSize(input_texture, 0));
    float result = 0.0;
    const int h = 2;
    uint n_samples = 0u;
    for (int x = -h; x <= h; ++x) {
        for (int y = -h; y <= h; ++y) {
            vec2 offset = vec2(float(x), float(y)) * texel_size;
            float sample = texture(input_texture, texcoord + offset).x;
            if (sample != 0.0) {
                result += sample;
                ++n_samples;
            }
        }
    }
    blurred_texture = result / float(n_samples);
}

#endif
