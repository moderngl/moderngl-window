from pathlib import Path
import numpy as np
import random

import moderngl
import moderngl_window
from moderngl_window.opengl.vao import VAO
from moderngl_window import geometry


class Boids2(moderngl_window.WindowConfig):
    """Minimal WindowConfig example"""
    gl_version = (3, 3)
    window_size = 256, 256
    aspect_ratio = 1.0
    title = "Basic Window Config"
    resource_dir = (Path(__file__) / '../../resources').absolute()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Offscreen buffers
        self.texture_1 = self.ctx.texture(self.wnd.buffer_size, 4, dtype='f4')
        self.texture_2 = self.ctx.texture(self.wnd.buffer_size, 4, dtype='f4')
        self.fbo_1 = self.ctx.framebuffer(color_attachments=[self.texture_1])
        self.fbo_2 = self.ctx.framebuffer(color_attachments=[self.texture_1])

        # VAOs
        self.quad_fs = geometry.quad_fs()

        N = 1000
        def gen_boids(n):
            for i in range(n):
                yield random.uniform(-1, 1)
                yield random.uniform(-1, 1)
                yield random.uniform(-1, 1)
                yield random.uniform(-1, 1)

        data = np.fromiter(gen_boids(N), dtype='f4', count=N * 4)
        self.boids_buffer_1 = self.ctx.buffer(data=data)
        self.boids_buffer_2 = self.ctx.buffer(reserve=data.nbytes)

        self.boids_vao_1 = VAO(name='boids_1')
        self.boids_vao_1.buffer(self.boids_buffer_1, '2f 2f', ['in_position', 'in_velocity'])

        self.boids_vao_2 = VAO(name='boids_2')
        self.boids_vao_2.buffer(self.boids_buffer_2, '2f 2f', ['in_position', 'in_velocity'])

        # Programs
        self.tex_prog = self.load_program('programs/texture.glsl')
        self.tex_prog['texture0'].value = 0
        self.boid_points = self.load_program('programs/boids2/boid_points.glsl')
        # self.boid_locality = self.load_program('programs/boids2/boids_locality_info.glsl')

    def render(self, time, frametime):
        self.fbo_1.use()
        # Render initial data to framebuffer
        self.boids_vao_1.render(self.boid_points, mode=moderngl.POINTS)

        # debug render fbo
        self.wnd.fbo.use()
        self.texture_1.use(location=0)
        self.quad_fs.render(self.tex_prog)

        # Gather locality info
        # ..


if __name__ == '__main__':
    moderngl_window.run_window_config(Boids2)
