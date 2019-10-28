from pathlib import Path
import random
import numpy
from pyrr import matrix44

import moderngl
import moderngl_window
from moderngl_window.opengl.vao import VAO


class Boids(moderngl_window.WindowConfig):
    """
    An attempt to make something boid-list with GL3.3.
    Not currently working as intended, but still creates
    and interesting result.

    For this to properly work we need to split the calculations
    into several passes.

    We are doing this the O(n^2) way with the gpu using transform feedback.
    To make the data avaialble to the vertex shader (looping through it)
    we copy the vertex buffer every frame to a texture.

    A better way in the future is to use compute shader.
    """
    title = "Boids"
    resource_dir = (Path(__file__) / '../../resources').absolute()
    aspect_ratio = 3440 / 1440

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        MAX_TEX_WIDTH = 8192
        N = MAX_TEX_WIDTH * 1

        def gen_initial_data(n, x_area=2.0, y_area=2.0):
            for n in range(n):
                # position
                yield (random.random() - 0.5) * x_area
                yield (random.random() - 0.5) * y_area
                # Velocity
                yield (random.random() - 0.5)
                yield (random.random() - 0.5)

        # Create geometry data
        gen = gen_initial_data(N, x_area=self.aspect_ratio * 2 * 0.9, y_area=2.0 * 0.95)
        data = numpy.fromiter(gen, count=N * 4, dtype='f4')
        self.boids_buffer_1 = self.ctx.buffer(data.tobytes())
        self.boids_buffer_2 = self.ctx.buffer(data=self.boids_buffer_1.read())

        self.boids_vao_1 = VAO(name='boids_1', mode=moderngl.POINTS)
        self.boids_vao_1.buffer(self.boids_buffer_1, '2f 2f', ['in_position', 'in_velocity'])

        self.boids_vao_2 = VAO(name='boids_2', mode=moderngl.POINTS)
        self.boids_vao_2.buffer(self.boids_buffer_2, '2f 2f', ['in_position', 'in_velocity'])

        self.boids_texture = self.ctx.texture((MAX_TEX_WIDTH, N * 2 // MAX_TEX_WIDTH), components=2, dtype='f4')

        # Programs
        self.boids_render_program = self.load_program('programs/boids/boids_render.glsl')
        self.boids_transform_program = self.load_program('programs/boids/boids_transform.glsl')

        # Prepare for rendering
        self.m_proj = matrix44.create_orthogonal_projection(
            -self.aspect_ratio, self.aspect_ratio,
            -1.0, 1.0,
            -1.0, 1.0,
            dtype='f4',
        )
        self.boids_render_program['m_proj'].write(self.m_proj.tobytes())
        self.boids_transform_program['data'].value = 0
        self.boids_transform_program['num_boids'].value = N
        self.boids_transform_program['tex_width'].value = MAX_TEX_WIDTH

    def render(self, time, frame_time):

        self.boids_texture.use(location=0)
        self.boids_transform_program['timedelta'].value = frame_time  # max(frame_time, 1.0 / 60.0)
        self.boids_vao_1.transform(self.boids_transform_program, self.boids_buffer_2)
        self.boids_vao_2.render(self.boids_render_program)

        # Swap around ..
        self.boids_vao_1, self.boids_vao_2 = self.boids_vao_2, self.boids_vao_1
        self.boids_buffer_1, self.boids_buffer_2 = self.boids_buffer_2, self.boids_buffer_1

        # Write vertex data into texture so we can interate it in shader
        self.boids_texture.write(self.boids_buffer_1.read())


if __name__ == '__main__':
    moderngl_window.run_window_config(Boids)
