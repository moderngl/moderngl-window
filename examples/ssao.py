import numpy as np
from pathlib import Path
from pyrr import Matrix44

import moderngl
import moderngl_window
from base import OrbitCameraWindow


class SSAODemo(OrbitCameraWindow):
    title = "SSAO"
    resource_dir = (Path(__file__) / '../resources').resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True

        self.camera.projection.update(near=0.1, far=50.0)
        self.camera.radius = 3.0
        self.camera.angle_x = 290.0
        self.camera.angle_y = -80.0
        self.camera.velocity = 7.0
        self.camera.target = (0.0, 0.0, 0.0)
        self.camera.mouse_sensitivity = 0.3

        self.ssao_z_offset = 0.0

        # Create the geometry framebuffer.
        self.g_view_z = self.ctx.texture(self.wnd.buffer_size, 1, dtype="f2")
        self.g_normal = self.ctx.texture(self.wnd.buffer_size, 3, dtype="f2")
        self.g_depth = self.ctx.depth_texture(self.wnd.buffer_size)
        self.g_buffer = self.ctx.framebuffer(
            color_attachments=[self.g_view_z, self.g_normal],
            depth_attachment=self.g_depth
        )

        # Generate the SSAO framebuffer.
        self.ssao_occlusion = self.ctx.texture(self.wnd.buffer_size, 1, dtype="f1")
        self.ssao_buffer = self.ctx.framebuffer(color_attachments=[self.ssao_occlusion])

        # Generate the blurred SSAO framebuffer.
        self.ssao_blurred_occlusion = self.ctx.texture(self.wnd.buffer_size, 1, dtype="f1")
        self.ssao_blurred_buffer = self.ctx.framebuffer(
            color_attachments=[self.ssao_blurred_occlusion]
        )

        # Load the geometry program.
        self.geometry_program = self.load_program("programs/ssao/geometry.glsl")

        # Load the SSAO program.
        self.ssao_program = self.load_program("programs/ssao/ssao.glsl")
        self.ssao_program["g_view_z"].value = 0
        self.ssao_program["g_norm"].value = 1
        self.ssao_program["noise"].value = 2

        # Load the blurring program.
        self.blur_program = self.load_program("programs/ssao/blur.glsl")
        self.blur_program["input_texture"].value = 0

        # Load the shading program.
        self.shading_program = self.load_program("programs/ssao/shading.glsl")
        self.shading_program["g_view_z"].value = 0
        self.shading_program["g_normal"].value = 1
        self.shading_program["ssao_occlusion"].value = 2

        # Load the scene.
        self.scene = self.load_scene('scenes/stanford_dragon.obj')
        self.vao = self.scene.root_nodes[0].mesh.vao.instance(self.geometry_program)

        # Generate a fullscreen quad.
        self.quad_fs = moderngl_window.geometry.quad_fs()

        # Generate SSAO samples (in tangent space coordinates, with z along the normal).
        self.n_ssao_samples = 64 # If you change this number, also change ssao.glsl.
        self.ssao_std_dev = 0.5
        self.ssao_samples = np.random.normal(0.0, self.ssao_std_dev, (self.n_ssao_samples, 3))
        self.ssao_samples[:, 2] = np.abs(self.ssao_samples[:, 2])
        self.ssao_program["samples"].write(self.ssao_samples.ravel().astype('f4'))

        # Create random vectors used to decorrelate SSAO samples.
        rand_texture_size = 32 # If you change this number, also change ssao.glgl.
        rand_texture_data = np.random.bytes(3 * rand_texture_size * rand_texture_size)
        self.random_texture = self.ctx.texture(
            (rand_texture_size, rand_texture_size),
            3,
            dtype="f1",
            data=rand_texture_data
        )
        self.random_texture.filter == (moderngl.NEAREST, moderngl.NEAREST)
        self.random_texture.repeat_x = True
        self.random_texture.repeat_y = True

    def render(self, time: float, frametime: float):
        projection_matrix = self.camera.projection.matrix
        camera_matrix = self.camera.matrix
        mvp = projection_matrix * camera_matrix
        camera_pos = (self.camera.position.x, self.camera.position.y, self.camera.position.z)

        # Run the geometry pass.
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.g_buffer.clear(0.0, 0.0, 0.0)
        self.g_buffer.use()
        self.geometry_program["mvp"].write(mvp.astype('f4'))
        self.geometry_program["m_camera"].write(camera_matrix.astype('f4'))
        self.vao.render()

        # Calculate occlusion.
        self.ctx.disable(moderngl.DEPTH_TEST)
        self.ssao_buffer.clear(0.0)
        self.ssao_buffer.use()
        self.ssao_program["m_camera_inverse"].write(camera_matrix.inverse.astype('f4'))
        self.ssao_program["m_projection_inverse"].write(projection_matrix.inverse.astype('f4'))
        self.ssao_program["v_camera_pos"].value = camera_pos
        self.ssao_program["f_camera_pos"].value = camera_pos
        self.ssao_program["mvp"].write(mvp.astype('f4'))
        self.ssao_program["z_offset"].value = self.ssao_z_offset
        self.g_view_z.use(location=0)
        self.g_normal.use(location=1)
        self.random_texture.use(location=2)
        self.quad_fs.render(self.ssao_program)

        # Blur the occlusion map.
        self.ssao_blurred_buffer.clear(0.0)
        self.ssao_blurred_buffer.use()
        self.ssao_occlusion.use(location=0)
        self.quad_fs.render(self.blur_program)

        # Run the shading pass.
        self.ctx.screen.clear(1.0, 1.0, 1.0);
        self.ctx.screen.use()
        self.shading_program["m_camera_inverse"].write(camera_matrix.inverse.astype('f4'))
        self.shading_program["m_projection_inverse"].write(projection_matrix.inverse.astype('f4'))
        self.shading_program["v_camera_pos"].value = camera_pos
        self.shading_program["camera_pos"].value = camera_pos
        self.shading_program["light_pos"].value = camera_pos
        self.g_view_z.use(location=0)
        self.g_normal.use(location=1)
        self.ssao_blurred_occlusion.use(location=2)
        self.quad_fs.render(self.shading_program)


if __name__ == '__main__':
    moderngl_window.run_window_config(SSAODemo)
