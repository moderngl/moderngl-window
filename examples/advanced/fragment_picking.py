import struct
from pathlib import Path

import moderngl
import glm
import moderngl_window
from moderngl_window import geometry
from moderngl_window.opengl.projection import Projection3D
from moderngl_window.opengl.vao import VAO


class FragmentPicking(moderngl_window.WindowConfig):
    """
    Demonstrates how you can pick exact positions on a model
    efficiently using the gpu. We render the scene info
    to various layers in an offscreen framebuffer and
    use this to fetch the view position of the picked
    fragment. We can then apply the inverse modelview
    to create points positions that matches the original mesh.

    In this example we pick points on a mesh mapped with
    a texture containing heat information. We pick the
    position, heat value and the normal of the fragment.
    The normal is then used to hide points that point
    away from the camera.
    """

    title = "Fragment Picking"
    gl_version = 3, 3
    window_size = 1280, 720
    aspect_ratio = None
    resizable = True
    resource_dir = (Path(__file__) / "../../resources").resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("window buffer size:", self.wnd.buffer_size)
        self.marker_file = Path("markers.bin")
        # Object rotation
        self.x_rot = 0
        self.y_rot = 0
        # Object position
        self.zoom = 0

        # Load scene cached to speed up loading!
        self.scene = self.load_scene("scenes/fragment_picking/centered.obj", cache=True)
        # Grab the raw mesh/vertexarray
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
        self.offscreen_normals = self.ctx.texture(self.wnd.buffer_size, 4, dtype="f2")
        # Texture for storing the view positions rendered to framebuffer
        self.offscreen_viewpos = self.ctx.texture(self.wnd.buffer_size, 4, dtype="f4")
        # Texture for storing depth values
        self.offscreen_depth = self.ctx.depth_texture(self.wnd.buffer_size)
        # Create a framebuffer we can render to
        self.offscreen = self.ctx.framebuffer(
            color_attachments=[
                self.offscreen_diffuse,
                self.offscreen_normals,
                self.offscreen_viewpos,
            ],
            depth_attachment=self.offscreen_depth,
        )

        # This is just for temp changing depth texture parameters
        # temporary so we can use it as a normal texture
        self.depth_sampler = self.ctx.sampler(
            filter=(moderngl.LINEAR, moderngl.LINEAR),
            compare_func="",
        )

        # A fullscreen quad just for rendering offscreen textures to the window
        self.quad_fs = geometry.quad_fs()

        # --- Shaders
        # Simple program just rendering texture
        self.texture_program = self.load_program("programs/fragment_picking/texture.glsl")
        self.texture_program["texture0"].value = 0
        # Geomtry shader writing to two offscreen layers (color, normal) + depth
        self.geometry_program = self.load_program("programs/fragment_picking/geometry.glsl")
        self.geometry_program["texture0"].value = 0  # use texture channel 0

        # Shader for linearizing depth (debug visualization)
        self.linearize_depth_program = self.load_program("programs/linearize_depth.glsl")
        self.linearize_depth_program["texture0"].value = 0
        self.linearize_depth_program["near"].value = self.projection.near
        self.linearize_depth_program["far"].value = self.projection.far

        # Shader for picking the world position of a fragment
        self.fragment_picker_program = self.load_program("programs/fragment_picking/picker.glsl")
        self.fragment_picker_program["position_texture"].value = 0  # Read from texture channel 0
        self.fragment_picker_program["normal_texture"].value = 1  # Read from texture channel 1
        self.fragment_picker_program["diffuse_texture"].value = 2  # Read from texture channel 2

        # Picker geometry
        self.marker_byte_size = 7 * 4  # position + normal + temperature (7 x 32bit floats)
        self.picker_output = self.ctx.buffer(reserve=self.marker_byte_size)
        self.picker_vao = VAO(mode=moderngl.POINTS)

        # Shader for rendering markers
        self.marker_program = self.load_program("programs/fragment_picking/markers.glsl")
        self.marker_program["color"].value = 1.0, 0.0, 0.0, 1.0

        # Marker geometry
        self.marker_buffer = self.ctx.buffer(
            reserve=self.marker_byte_size * 1000
        )  # Resever room for 1000 points
        self.marker_vao = VAO(name="markers", mode=moderngl.POINTS)
        self.marker_vao.buffer(
            self.marker_buffer, "3f 3f 1f", ["in_position", "in_normal", "temperature"]
        )
        self.num_markers = 0

        # Debug geometry
        self.quad_normals = geometry.quad_2d(size=(0.25, 0.25), pos=(0.75, 0.875))
        self.quad_depth = geometry.quad_2d(size=(0.25, 0.25), pos=(0.5, 0.875))
        self.quad_positions = geometry.quad_2d(size=(0.25, 0.25), pos=(0.25, 0.875))

    def render(self, time, frametime):
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        translation = glm.translate(glm.vec3(0, 0, -45 + self.zoom))
        rotation = glm.mat4(glm.quat(glm.vec3(self.y_rot, self.x_rot, 0)))
        self.modelview = translation * rotation

        # Render the scene to offscreen buffer
        self.offscreen.clear()
        self.offscreen.use()

        # Render the scene
        self.geometry_program["modelview"].write(self.modelview)
        self.geometry_program["projection"].write(self.projection.matrix)
        self.mesh_texture.use(location=0)  # bind texture from obj file to channel 0
        self.depth_sampler.use(location=0)
        self.mesh.render(self.geometry_program)  # render mesh
        self.depth_sampler.clear(location=0)

        # Activate the window as the render target
        self.ctx.screen.use()
        self.ctx.disable(moderngl.DEPTH_TEST)

        # Render offscreen diffuse layer to screen
        self.offscreen_diffuse.use(location=0)
        self.quad_fs.render(self.texture_program)

        # Render markers
        if self.num_markers > 0:
            self.ctx.point_size = 6.0  # Specify fragment size of the markers
            self.marker_program["modelview"].write(self.modelview)
            self.marker_program["projection"].write(self.projection.matrix)
            self.marker_vao.render(self.marker_program, vertices=self.num_markers)

        self.render_debug()

    def render_debug(self):
        """Debug rendering. Offscreen buffers"""
        # Debug rendering of normal and depth buffer
        self.offscreen_normals.use()
        self.quad_normals.render(self.texture_program)

        self.offscreen_depth.use(location=0)  # bind depth sampler to channel 0
        self.depth_sampler.use(location=0)  # temp override the parameters
        self.quad_depth.render(self.linearize_depth_program)
        self.depth_sampler.clear(location=0)  # Remove the override

        self.offscreen_viewpos.use()
        self.quad_positions.render(self.texture_program)

    def mouse_drag_event(self, x, y, dx, dy):
        """Pick up mouse drag movements"""
        self.x_rot -= dx / 100
        self.y_rot -= dy / 100

    def mouse_press_event(self, x, y, button):
        """Attempts to get the view position from a fragment"""

        # only care about right mouse button clicks
        if button != self.wnd.mouse.right:
            return

        # mouse coordinates starts in upper left corner
        # pixel positions starts and lower left corner
        pos = int(x * self.wnd.pixel_ratio), int(
            self.wnd.buffer_height - (y * self.wnd.pixel_ratio)
        )
        print("Picking mouse position", x, y)
        print("Viewport position", pos)

        self.fragment_picker_program["texel_pos"].value = pos
        self.fragment_picker_program["modelview"].write(self.modelview)
        self.offscreen_viewpos.use(location=0)
        self.offscreen_normals.use(location=1)
        self.offscreen_diffuse.use(location=2)
        self.picker_vao.transform(self.fragment_picker_program, self.picker_output, vertices=1)

        # Print position
        x, y, z, nx, ny, nz, temperature = struct.unpack("7f", self.picker_output.read())
        if z == 0.0:
            print("Point is not on the mesh")
            return

        print(f"Position: {x} {y} {z}")
        print(f"Normal: {nx} {ny} {nz}")
        print(f"Temperature: {round(temperature * 255)} (byte) {temperature} (float)")
        self.marker_buffer.write(
            self.picker_output.read(), offset=self.marker_byte_size * self.num_markers
        )
        self.num_markers += 1

    def mouse_scroll_event(self, x_offset, y_offset):
        self.zoom += y_offset

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        # Key presses
        if action == keys.ACTION_PRESS:
            if key == keys.F1:
                print("Loading marker file")
                self.load_markers(self.marker_file)

            if key == keys.F2:
                print("Saving marker file")
                self.save_markers(self.marker_file)

    def load_markers(self, path: Path):
        """Loads markers from file"""
        if not self.marker_file.exists():
            return

        with open(self.marker_file, mode="rb") as fd:
            size = self.marker_file.stat().st_size
            self.num_markers = size // self.marker_byte_size
            self.marker_buffer.write(fd.read(), offset=0)

    def save_markers(self, path: Path):
        """Dump markers from file"""
        if self.num_markers == 0:
            return

        with open("markers.bin", mode="wb") as fd:
            fd.write(self.marker_buffer.read(size=self.num_markers * self.marker_byte_size))


if __name__ == "__main__":
    moderngl_window.run_window_config(FragmentPicking)
