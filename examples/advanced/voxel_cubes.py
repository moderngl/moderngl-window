"""
Simple voxel cube renderer using instancing.

* A lookup texture decides what cubes are active
* A transform shader generates the per-instance data (for instanced draw).
  This transform only emits active cubes based on the texture lookup.
  This transform also remove cubes having 6 neighbors.

We can render the voxel with simple light or wireframe.

The point of this example is to :
* Show how voxel data can be generated on the GPU
* Show how textures can be used as useful lookup structures
* Partial texture updates from client
* We can reduce a voxel volume dramatically by just inspecting neighbors
"""

from array import array
from pathlib import Path

import glm
import moderngl
from base import CameraWindow

from moderngl_window import geometry


class CubeVoxel(CameraWindow):
    name = "Cube Voxel"
    window_size = 1920, 1080
    resource_dir = (Path(__file__) / "../../resources").resolve()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera.projection.update(near=1, far=500)
        self.camera.velocity = 50
        self.wnd.mouse_exclusivity = True

        s = 100  # FIXME: NOT TESTED WITH OTHER VALUES
        self.voxel = Voxel(ctx=self.ctx, size=(s, s, s))
        # Load resources for the voxel instance
        self.voxel.texture_prog = self.load_program("programs/texture.glsl")
        self.voxel.gen_instance_prog = self.load_program(
            "programs/voxel_cubes/gen_voxel_instance_data.glsl"
        )
        self.voxel.voxel_light_prog = self.load_program(
            "programs/voxel_cubes/voxel_light.glsl"
        )
        self.voxel.voxel_wireframe_prog = self.load_program(
            "programs/voxel_cubes/voxel_wireframe.glsl"
        )

        self.wireframe = True
        self.voxel.rebuild()
        self.current_layer = 0
        self.fill = False

    def render(self, time, frame_time):
        self.ctx.clear()
        # Render the lookup texture in the background
        self.ctx.enable_only(moderngl.NOTHING)
        self.voxel.render_lookup_texture()

        # Render the voxel
        if self.wireframe:
            self.ctx.enable_only(moderngl.NOTHING)
            self.voxel.render_wireframe(
                projection_matrix=self.camera.projection.matrix,
                camera_matrix=self.camera.matrix,
            )
        else:
            self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
            self.voxel.render(
                projection_matrix=self.camera.projection.matrix,
                camera_matrix=self.camera.matrix,
            )

        # Update some data in the voxel
        if self.fill:
            self.voxel.fill_layer(self.current_layer, 255)
        else:
            self.voxel.fill_layer(self.current_layer, 0)

        self.voxel.rebuild()

        self.current_layer += 1
        if self.current_layer == 100:
            self.fill = not self.fill
            self.current_layer = 0


class Voxel:
    """
    Simple cube voxel implementation using OpenGL 3.3 core.
    We are sticking to simple transforms at textures.
    """

    def __init__(self, *, ctx: moderngl.Context, size: tuple[int, int, int]):
        self.ctx = ctx
        self._size = size

        # Create lookup texture for active blocks
        # NOTE: We allocate room for 100 x 100 x 100 for now
        #       100 x 100 x 100 = 1_000_000 fragments
        #       1000 x 1000 = 1_000_000 fragments
        #       We store several 100 x 100 layers respersting one slice in voxel
        self.voxel_lookup = self.ctx.texture((1000, 1000), 1, dtype="f1")
        self.voxel_lookup.filter = moderngl.NEAREST, moderngl.NEAREST
        self.voxel_lookup.repeat_x = False
        self.voxel_lookup.repeat_y = False
        # Write in some default data
        for i in range(100):
            self.fill_layer(i, 255)

        # Construct the per-instance data for active cubes using a transform
        self.instance_data = ctx.buffer(reserve=self.max_cubes * 4 * 3)

        self.quad_fs = geometry.quad_fs()
        self.gen_instance_vao = None

        self._num_instances = 0
        self._query = self.ctx.query(primitives=True)

        self.cube = geometry.cube()
        self.cube.buffer(self.instance_data, "3f/i", ["in_offset"])
        # Filled externally
        self.texture_prog = None
        self.gen_instance_prog = None
        self.voxel_light_prog = None
        self.voxel_wireframe_prog = None

    @property
    def max_cubes(self) -> int:
        return self._size[0] * self._size[1] * self._size[2]

    def render_wireframe(self, *, projection_matrix, camera_matrix, model_matrix=None):
        self.ctx.wireframe = True
        translate = glm.translate(
            glm.vec3(-self._size[0] / 2, -self._size[0] / 2, -self._size[0] * 2),
        )
        mat = camera_matrix * translate
        self.voxel_wireframe_prog["m_proj"].write(projection_matrix)
        self.voxel_wireframe_prog["m_modelview"].write(mat)
        self.cube.render(self.voxel_wireframe_prog, instances=self._num_instances)
        self.ctx.wireframe = False

    def render(self, *, projection_matrix, camera_matrix, model_matrix=None):
        """Render out the voxel to the screen"""

        translate = glm.translate(
            glm.vec3(-self._size[0] / 2, -self._size[0] / 2, -self._size[0] * 2),
        )
        mat = camera_matrix * translate
        normal = glm.transpose(glm.inverse(glm.mat3(mat))).to_bytes()
        self.voxel_light_prog["m_proj"].write(projection_matrix)
        self.voxel_light_prog["m_modelview"].write(mat)
        self.voxel_light_prog["m_normal"].write(normal)
        self.cube.render(self.voxel_light_prog, instances=self._num_instances)

    def render_lookup_texture(self):
        """Display the lookup texture as a fullscreen quad"""
        self.voxel_lookup.use()
        self.quad_fs.render(self.texture_prog)

    def rebuild(self):
        """Rebuild the voxel. This is necessary when the lookup texture has been altered"""
        if not self.gen_instance_vao:
            self.gen_instance_vao = self.ctx.vertex_array(self.gen_instance_prog, [])

        self.gen_instance_prog["voxel_size"] = self._size
        self.voxel_lookup.use(location=0)
        with self._query:
            self.gen_instance_vao.transform(
                self.instance_data, mode=moderngl.POINTS, vertices=self.max_cubes
            )
        self._num_instances = self._query.primitives

    def fill_layer(self, layer: int, value: int):
        x = (layer % 10) * self._size[0]
        y = (layer // 10) * self._size[1]
        self.voxel_lookup.write(
            array("B", [value] * 100 * 100), viewport=(x, y, 100, 100)
        )

    # NOTE: These functions can make adding and removing cubes extremely fast
    def add_cubes(self, positions):
        """Render to the lookup texture"""
        pass

    def remove_cubes(self, positions):
        """Render to the lookup texture"""
        pass


if __name__ == "__main__":
    CubeVoxel.run()
