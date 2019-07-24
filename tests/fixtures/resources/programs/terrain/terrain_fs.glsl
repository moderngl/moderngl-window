#version 410

out vec4 fragColor;
in vec2 ts_uv;
uniform sampler2D heightmap;

void main() {
    float color = texture(heightmap, ts_uv).r;
    fragColor = vec4(color);
}
