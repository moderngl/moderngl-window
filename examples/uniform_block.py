from pyrr import Matrix44, matrix44, Vector3

import moderngl
import moderngl_window as mglw
from moderngl_window import geometry


class CubeSimple(mglw.WindowConfig):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cube = geometry.cube(size=(2, 2, 2))
        shader_source = {
            'vertex_shader': '''
                #version 330

                in vec3 in_position;
                in vec3 in_normal;

                uniform vec3 pos_offset;

                uniform Projection {
                    uniform mat4 matrix;
                } proj;

                uniform View {
                    uniform mat4 matrix;
                } view;

                out vec3 normal;
                out vec3 pos;

                void main() {
                    vec4 p = view.matrix * vec4(in_position + pos_offset, 1.0);
                    gl_Position =  proj.matrix * p;
                    mat3 m_normal = transpose(inverse(mat3(view.matrix)));
                    normal = m_normal * in_normal;
                    pos = p.xyz;
                }
            ''',
            'fragment_shader': '''
                #version 330

                out vec4 color;

                in vec3 normal;
                in vec3 pos;

                void main() {
                    float l = dot(normalize(-pos), normalize(normal));
                    color = vec4(1.0) * (0.25 + abs(l) * 0.75);
                }
            ''',
        }
        self.prog1 = self.ctx.program(**shader_source)
        self.prog1['pos_offset'].value = (1.1, 0, 0)
        self.prog2 = self.ctx.program(**shader_source)
        self.prog2['pos_offset'].value = (-1.1, 0, 0)

        self.vao1 = self.cube.instance(self.prog1)
        self.vao2 = self.cube.instance(self.prog2)

        self.m_proj = matrix44.create_perspective_projection_matrix(
            75, self.wnd.aspect_ratio,  # fov, aspect
            0.1, 100.0,  # near, far
            dtype='f4',
        )

        proj_uniform1 = self.prog1['Projection']
        view_uniform1 = self.prog1['View']
        proj_uniform2 = self.prog2['Projection']
        view_uniform2 = self.prog2['View']

        self.proj_buffer = self.ctx.buffer(reserve=proj_uniform1.size)
        self.view_buffer = self.ctx.buffer(reserve=view_uniform1.size)

        proj_uniform1.binding = 1
        view_uniform1.binding = 2
        proj_uniform2.binding = 1
        view_uniform2.binding = 2

        self.proj_buffer.write(self.m_proj.tobytes())

        self.scope1 = self.ctx.scope(
            self.ctx.fbo,
            enable_only=moderngl.CULL_FACE | moderngl.DEPTH_TEST,
            uniform_buffers=[
                (self.proj_buffer, 1),
                (self.view_buffer, 2),
            ],
        )

        self.scope2 = self.ctx.scope(
            self.ctx.fbo,
            enable_only=moderngl.CULL_FACE | moderngl.DEPTH_TEST,
            uniform_buffers=[
                (self.proj_buffer, 1),
                (self.view_buffer, 2),
            ],
        )

    def render(self, time=0.0, frametime=0.0, target: moderngl.Framebuffer = None):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        m_rot = Matrix44.from_eulers(Vector3((time, time, time)))
        m_trans = matrix44.create_from_translation(Vector3((0.0, 0.0, -5.0)))
        m_modelview = matrix44.multiply(m_rot, m_trans)

        self.view_buffer.write(m_modelview.astype('f4').tobytes())

        with self.scope1:
            self.vao1.render(mode=moderngl.TRIANGLES)

        with self.scope2:
            self.vao2.render(mode=moderngl.TRIANGLES)


if __name__ == '__main__':
    mglw.run_window_config(CubeSimple)
