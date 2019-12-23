import struct
from pathlib import Path

import moderngl
from pyrr import Matrix44
import moderngl_window
from moderngl_window import geometry
from moderngl_window.opengl.projection import Projection3D
from moderngl_window.opengl.vao import VAO


class FragmentPicking(moderngl_window.WindowConfig):
    title = "Fragment Picking"
    gl_version = 3, 3
    window_size = 1280, 720
    resizable = False
    resource_dir = (Path(__file__) / '../../resources').resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Object rotation
        self.x_rot = 0
        self.y_rot = 0

        # Load scene cached to speed up loading!
        self.scene = self.load_scene('scenes/fragment_picking/centered.obj', cache=True)
        # Grab the raw mesh
        self.mesh = self.scene.root_nodes[0].mesh.vao
        self.mesh_texture = self.scene.root_nodes[0].mesh.material.mat_texture.texture

        self.projection = Projection3D(
            fov=60,
            aspect_ratio=self.wnd.aspect_ratio,
            near=1.0,
            far=100.0,
        )

        # --- Offscreen render target
        # RGBA color/diffuse layer
        self.offscreen_diffuse = self.ctx.texture(self.wnd.buffer_size, 4)
        # Textures for storing normals (16 bit floats)
        self.offscreen_normals = self.ctx.texture(self.wnd.buffer_size, 4)  # , dtype='f2')
        # Texture for storing depth values
        self.offscreen_depth = self.ctx.depth_texture(self.wnd.buffer_size)
        # Create a framebuffer we can render to
        self.offscreen = self.ctx.framebuffer(
            color_attachments=[
                self.offscreen_diffuse,
                self.offscreen_normals,
            ],
            depth_attachment=self.offscreen_depth,
        )

        # A fullscreen quad just for rendering offscreen colors to the window
        self.quad_fs = geometry.quad_fs()

        # --- Shaders
        # Simple program just rendering texture
        self.texture_program = self.load_program('programs/fragment_picking/texture.glsl')
        # Geomtry shader writing to two offscreen layers (color, normal) + depth
        self.geometry_program = self.load_program('programs/fragment_picking/geometry.glsl')
        self.geometry_program['projection'].write(self.projection.matrix)

        # Shader for linearizing depth (debug visualization)
        self.linearize_depth_program = self.load_program('programs/fragment_picking/linearize_depth.glsl')
        self.linearize_depth_program['near'].value = self.projection.near
        self.linearize_depth_program['far'].value = self.projection.far

        # Shader for picking the world position of a fragment
        self.fragment_picker_program = self.load_program('programs/fragment_picking/picker.glsl')
        self.fragment_picker_program['proj_const'].value = self.projection.projection_constants

        # Picker geometry
        self.picker_input = self.ctx.buffer(reserve=12)
        self.picker_output = self.ctx.buffer(reserve=12)
        self.picker_vao = VAO(mode=moderngl.POINTS)
        self.picker_vao.buffer(self.picker_input, '3f', ['in_position'])

        # Debug geometry
        self.quad_normals = geometry.quad_2d(size=(0.5, 0.5), pos=(0.75, 0.75))
        self.quad_depth = geometry.quad_2d(size=(0.5, 0.5), pos=(0.25, 0.75))

    def render(self, time, frametime):
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        translation = Matrix44.from_translation((0, 0, -45), dtype='f4')
        rotation = Matrix44.from_eulers((self.y_rot, self.x_rot, 0), dtype='f4')
        self.modelview = translation * rotation

        # Render the scene to offscreen buffer
        # self.offscreen.clear()
        # self.offscreen.use()

        # Render the scene
        # self.geometry_program['modelview'].write(self.modelview)
        # self.mesh_texture.use()
        # self.mesh.render(self.geometry_program)
        self.scene.draw(
            projection_matrix=self.projection.matrix,
            camera_matrix=self.modelview,
        )

        # self.ctx.disable(moderngl.DEPTH_TEST)

        # Activate the window as the render target
        # self.ctx.screen.use()

        # Render offscreen diffuse layer to screen
        # self.offscreen_diffuse.use()
        # self.quad_fs.render(self.texture_program)

        # self.render_debug()

    def render_debug(self):
        """Debug rendering. Offscreen buffers"""
        # Debug rendering of normal and depth buffer
        self.offscreen_normals.use()
        self.quad_normals.render(self.texture_program)

        self.offscreen_depth.use()
        self.offscreen_depth.filter = moderngl.NEAREST, moderngl.NEAREST
        self.offscreen_depth.compare_func = ''  # Turn off compare func to be able to read it
        self.quad_depth.render(self.linearize_depth_program)
        self.offscreen_depth.compare_func = '<='

    def mouse_drag_event(self, x, y, dx, dy):
        """Pick up mouse drag movements"""
        self.x_rot -= dx / 100
        self.y_rot -= dy / 100

    def mouse_press_event(self, x, y, button):
        """Attempts to get the view position from a fragment"""
        # mouse coordinates starts in upper left corner
        # pixel positions starts and lower left corner
        pos = int(x * self.wnd.pixel_ratio), int(self.wnd.buffer_height - y * self.wnd.pixel_ratio)
        print("Reading position", pos)
        self.fragment_picker_program['texel_pos'].value = pos
        self.picker_vao.transform(self.fragment_picker_program, self.picker_output, vertices=1)

        # Print position
        print(struct.unpack('3f', self.picker_output.read()))


if __name__ == '__main__':
    moderngl_window.run_window_config(FragmentPicking)
