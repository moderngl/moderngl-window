#version 330

#if defined VERTEX_SHADER

uniform mat4 m_camera_inverse;
uniform mat4 m_projection_inverse;
uniform vec3 v_camera_pos;

in vec3 in_position;
in vec2 in_texcoord_0;

out vec3 view_ray;
out vec2 texcoord;

void main() {
    gl_Position = vec4(in_position, 1.0);

    // Convert in_position from clip space to view space.
    vec4 pos = m_projection_inverse * vec4(in_position, 1.0);
    // Normalize its z value.
    pos.xy /= -pos.z;
    pos.z = -1.0;
    pos.w = 1.0;
    // Convert to world space.
    pos = m_camera_inverse * pos;
    view_ray = pos.xyz - v_camera_pos;

    texcoord = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

uniform vec3 light_pos;
uniform vec3 camera_pos;

uniform sampler2D g_view_z;
uniform sampler2D g_normal;
uniform sampler2D ssao_occlusion;

in vec3 view_ray;
in vec2 texcoord;

layout(location=0) out vec4 frag_color;

void main() {
    // Ignore background fragments.
    float view_z = texture(g_view_z, texcoord).x;
    if (view_z == 0.0) {
        discard;
    }

    // Load/compute the position and normal vectors (in world space).
    vec3 position = camera_pos + view_z * view_ray;
    vec3 normal = texture(g_normal, texcoord).xyz;

    // Compute lighting.
    float occlusion = texture(ssao_occlusion, texcoord).x;
    vec3 light_dir = normalize(light_pos - position);
    vec3 reflection_dir = reflect(-light_dir, normal);
    float ambient = 0.3 * occlusion;
    float diffuse = 0.5 * max(dot(light_dir, normal), 0.0);
    float specular = 0.4 * pow(max(dot(light_dir, normal), 0.0), 10.0);
    float luminosity = ambient + diffuse + specular;
    vec3 color = luminosity * vec3(0.2, 0.2, 0.6);
    color = vec3(occlusion);
    frag_color = vec4(color, 1.0);
}

#endif
