#version 330

out vec4 outColor;
in vec2 uv;
in vec3 geo_color;

uniform sampler2D texture0;

void main() {
    outColor = texture(texture0, uv) * vec4(geo_color, 1.0);
}
