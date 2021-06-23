#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in uint in_char_id;

uniform vec2 char_size;

out uint vs_char_id;

void main() {
    // float ypos = int(gl_InstanceID / line_length) * char_size.y;
    float xpos = gl_InstanceID * char_size.x;
	gl_Position = vec4(in_position + vec3(xpos, 0.0, 0.0), 1.0);
    vs_char_id = in_char_id;
}

#elif defined GEOMETRY_SHADER

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

uniform mat4 m_proj;
uniform vec2 text_pos;
uniform vec2 char_size;

in uint vs_char_id[1];
out vec2 uv;
flat out uint gs_char_id;

void main() {
    vec3 pos = gl_in[0].gl_Position.xyz + vec3(text_pos, 0.0);

    vec3 right = vec3(1.0, 0.0, 0.0) * char_size.x / 2.0;
    vec3 up = vec3(0.0, 1.0, 0.0) * char_size.y / 2.0;

    // upper right
    uv = vec2(1.0, 1.0);
    gs_char_id = vs_char_id[0];
    gl_Position = m_proj * vec4(pos + (right + up), 1.0);
    EmitVertex();

    // upper left
    uv = vec2(0.0, 1.0);
    gs_char_id = vs_char_id[0];
    gl_Position = m_proj * vec4(pos + (-right + up), 1.0);
    EmitVertex();

    // lower right
    uv = vec2(1.0, 0.0);
    gs_char_id = vs_char_id[0];
    gl_Position = m_proj * vec4(pos + (right - up), 1.0);
    EmitVertex();

    // lower left
    uv = vec2(0.0, 0.0);
    gs_char_id = vs_char_id[0];
    gl_Position = m_proj * vec4(pos + (-right - up), 1.0);
    EmitVertex();

    EndPrimitive();
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform sampler2DArray font_texture;
in vec2 uv;
flat in uint gs_char_id;

void main()
{
    fragColor = texture(font_texture, vec3(uv, gs_char_id));
}
#endif
