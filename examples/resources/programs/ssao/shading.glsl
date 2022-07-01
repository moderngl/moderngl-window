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
uniform vec3 base_color;
uniform vec4 material_properties;
uniform int render_mode;

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
    float ambient_magnitude = material_properties.x;
    float diffuse_magnitude = material_properties.y;
    float specular_magnitude = material_properties.z;
    float specular_exponent = material_properties.w;
    float occlusion;
    if (render_mode != 1) {
        occlusion = texture(ssao_occlusion, texcoord).x;
    } else {
        occlusion = 1.0;
    }
    vec3 light_dir = normalize(light_pos - position);
    vec3 reflection_dir = reflect(-light_dir, normal);
    float ambient = ambient_magnitude * occlusion;
    float diffuse = diffuse_magnitude * max(dot(light_dir, normal), 0.0);
    float specular = specular_magnitude * pow(max(dot(light_dir, normal), 0.0), specular_exponent);
    float luminosity = ambient + diffuse + specular;
    vec3 color = luminosity * base_color;
    if (render_mode == 2) {
        color = vec3(occlusion);
    }
    frag_color = vec4(color, 1.0);
}

#endif
