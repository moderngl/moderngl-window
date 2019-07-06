from pyrr import Matrix44, matrix44, Vector3

import moderngl
import moderngl_window as mglw
from moderngl_window import geometry


class CubeSimple(mglw.WindowConfig):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cube = geometry.cube(size=(2, 2, 2))
        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330

                in vec3 in_position;

                uniform mat4 m_mv;
                uniform mat4 m_proj;

                void main() {
                    gl_Position =  m_proj * m_mv * vec4(in_position, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                out vec4 color;

                void main() {
                    color = vec4(1.0);
                }
            ''',
        )
        self.m_proj = matrix44.create_perspective_projection_matrix(
            75, self.wnd.aspect_ratio,  # fov, aspect
            0.1, 100.0,  # near, far
            dtype='f4',
        )
        self.prog['m_proj'].write(self.m_proj.tobytes())

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        m_rot = Matrix44.from_eulers(Vector3((time, time, time)))
        m_trans = matrix44.create_from_translation(Vector3((0.0, 0.0, -3.0)))
        m_mv = matrix44.multiply(m_rot, m_trans)

        self.prog['m_mv'].write(m_mv.astype('f4').tobytes())
        self.cube.render(self.prog, mode=moderngl.TRIANGLES)


if __name__ == '__main__':
    mglw.run_window_config(CubeSimple)
