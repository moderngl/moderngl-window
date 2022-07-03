
import imgui
import numpy as np
from pathlib import Path

import moderngl
import moderngl_window
from base import OrbitDragCameraWindow
from moderngl_window.integrations.imgui import ModernglWindowRenderer


class SSAODemo(OrbitDragCameraWindow):
    """A demo of screen space ambient occlusion, based on https://learnopengl.com/Advanced-Lighting/SSAO

    Runs best with a discrete GPU! Integrated GPUs can struggle a bit with the deferred rendering
    pipeline.
    """

    title = "SSAO"
    resource_dir = (Path(__file__) / '../resources').resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.wnd.mouse_exclusivity = True

        self.camera.projection.update(near=0.1, far=50.0)
        self.camera.radius = 2.0
        self.camera.angle_x = 290.0
        self.camera.angle_y = -80.0
        self.camera.velocity = 7.0
        self.camera.target = (0.0, 0.0, 0.0)
        self.camera.mouse_sensitivity = 1.0
        self.camera.zoom_sensitivity = 0.3

        self.render_modes = ["ADS + SSAO", "ADS (no SSAO)", "occlusion texture"]
        self.render_mode = 0
        self.base_color = (0.2, 0.4, 0.8)
        self.material_properties = [0.5, 0.5, 0.25, 25.0]
        self.ssao_z_offset = 0.0
        self.ssao_blur = False

        self.frame_time_decay_factor = 0.995
        self.average_frame_time = 0.01666

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
        self.scene = self.load_scene('scenes/stanford_dragon.obj', cache=True)
        self.vao = self.scene.root_nodes[0].mesh.vao.instance(self.geometry_program)

        # Generate a fullscreen quad.
        self.quad_fs = moderngl_window.geometry.quad_fs()

        # Generate SSAO samples (in tangent space coordinates, with z along the normal).
        self.n_ssao_samples = 64 # If you change this number, also change ssao.glsl.
        self.ssao_std_dev = 0.1
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

        # Set up imgui.
        imgui.create_context()
        if self.wnd.ctx.error != "GL_NO_ERROR":
           print(self.wnd.ctx.error)
        self.imgui = ModernglWindowRenderer(self.wnd)

    def render(self, time: float, frametime: float):
        self.average_frame_time = (self.frame_time_decay_factor * self.average_frame_time +
            (1.0 - self.frame_time_decay_factor) * frametime)

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
        if self.ssao_blur:
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
        self.shading_program["base_color"].value = tuple(self.base_color)
        self.shading_program["material_properties"].value = tuple(self.material_properties)
        self.shading_program["render_mode"].value = self.render_mode
        self.g_view_z.use(location=0)
        self.g_normal.use(location=1)
        if self.ssao_blur:
            self.ssao_blurred_occlusion.use(location=2)
        else:
            self.ssao_occlusion.use(location=2)
        self.quad_fs.render(self.shading_program)

        self.render_ui()

    def render_ui(self):
        imgui.new_frame()

        imgui.begin("Debug Panel", False)
        imgui.text(f"Frame time: {1000.0 * self.average_frame_time:.1f} ms")
        imgui.text(f"FPS: {1.0 / self.average_frame_time:.1f}")
        _, self.render_mode = imgui.combo("render mode", self.render_mode, self.render_modes)
        _, self.ssao_z_offset = imgui.slider_float("SSAO z-offset", self.ssao_z_offset, -0.3, 0.3)
        _, self.ssao_blur = imgui.checkbox("blur occlusion texture", self.ssao_blur)

        _, self.base_color = imgui.color_edit3(
            "color",
            self.base_color[0],
            self.base_color[1],
            self.base_color[2],
        )
        _, self.material_properties[0] = imgui.slider_float("ambient", self.material_properties[0], 0.0, 1.0)
        _, self.material_properties[1] = imgui.slider_float("diffuse", self.material_properties[1], 0.0, 1.0)
        _, self.material_properties[2] = imgui.slider_float("specular", self.material_properties[2], 0.0, 1.0)
        _, self.material_properties[3] = imgui.slider_float("specular exponent", self.material_properties[3], 1.0, 50.0)

        imgui.end()
        imgui.render()
        self.imgui.render(imgui.get_draw_data())

    def mouse_position_event(self, x, y, dx, dy):
        self.imgui.mouse_position_event(x, y, dx, dy)

    def mouse_drag_event(self, x: int, y: int, dx, dy):
        self.imgui.mouse_drag_event(x, y, dx, dy)
        if not self.imgui.io.want_capture_mouse:
            super().mouse_drag_event(x, y, dx, dy)

    def mouse_scroll_event(self, x_offset, y_offset):
        self.imgui.mouse_scroll_event(x_offset, y_offset)
        if not self.imgui.io.want_capture_mouse:
            super().mouse_scroll_event(x_offset, y_offset)

    def mouse_press_event(self, x, y, button):
        self.imgui.mouse_press_event(x, y, button)

    def mouse_release_event(self, x, y, button):
        self.imgui.mouse_release_event(x, y, button)

    def key_event(self, key, action, modifiers):
        self.imgui.key_event(key, action, modifiers)
        if not self.imgui.io.want_capture_keyboard:
            super().key_event(key, action, modifiers)


if __name__ == '__main__':
    moderngl_window.run_window_config(SSAODemo)
