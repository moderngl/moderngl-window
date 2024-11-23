from pathlib import Path
import numpy as np
import glm

import moderngl
from moderngl_window.opengl.vao import VAO
from moderngl_window import geometry
from base import CameraWindow


class VolumetricTetrahedralMesh(CameraWindow):
    """Volumetric Tetrahedral Mesh.

    The dataset was provided by:
    Mara Catalina Aguilera Canon at the Bournemouth University (UK).
    Area of research: Graph Neuro Networks, Finite Element Method

    An example rendering a volumetric mesh of the format:
    ``[[p1, p2, p3, p4], [p1, p2, p3, p4], ..]``
    were ```px``` represent a 3d point in a tetraherdon.
    A geometry shader calculates and emits the tetraherdons
    as triangles and calculate normals on the fly while rendering data.

    This helps us avoid doing this expensive operation
    in python and greatly reduces the memory requirement.

    Controls:
    - Camera: Mouse for rotation. AWSD + QE for translation
    - Press b to toggle blend mode on/off
    - Mouse wheel to increase or decrease the threshold for a tetra to be alive
    """

    gl_version = (4, 1)
    title = "Volumetric Tetrahedra lMesh"
    aspect_ratio = None
    resource_dir = (Path(__file__) / "../../resources").resolve()
    samples = 4

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Finetune camera
        self.wnd.mouse_exclusivity = True
        self.camera.projection.update(near=0.01, far=100)
        self.camera.mouse_sensitivity = 0.5
        self.camera.velocity = 2.5
        self.camera.projection.update(fov=60)

        # Scene states
        self.with_blending = False
        self.line_color = (0.0, 0.0, 0.0)
        self.mesh_color = (0.0, 0.8, 0.0)
        self.threshold = 0.5

        # For rendering background
        self.quad_fs = geometry.quad_fs()

        # (172575,) | 57,525 vertices
        vertices = np.load(self.resource_dir / "data/tetrahedral_mesh/mesh_nodes.npy")
        vertices = np.concatenate(vertices)
        # (259490, 4) (1037960,) indices
        indices = np.load(self.resource_dir / "data/tetrahedral_mesh/element_nodes.npy")
        indices = np.concatenate(indices) - 1

        # Probability of a tetrahedron is still alive
        w, h = 8192, int(np.ceil(indices.shape[0] / 8192))
        self.alive_data = np.random.random_sample(w * h)
        self.alive_texture = self.ctx.texture((w, h), 1, dtype="f2")
        self.alive_texture.write(self.alive_data.astype("f2"))

        # Original geometry with indices
        self.geometry = VAO(name="geometry_indices")
        self.geometry.buffer(vertices, "3f", "in_position")
        self.geometry.index_buffer(indices, index_element_size=4)

        self.prog_background = self.load_program("programs/tetrahedral_mesh/bg.glsl")
        self.prog_gen_tetra = self.load_program(
            vertex_shader="programs/tetrahedral_mesh/gen_tetra_vert.glsl",
            geometry_shader="programs/tetrahedral_mesh/gen_tetra_geo.glsl",
            fragment_shader="programs/tetrahedral_mesh/gen_tetra_frag.glsl",
        )
        self.prog_gen_tetra_lines = self.load_program(
            vertex_shader="programs/tetrahedral_mesh/gen_tetra_vert.glsl",
            geometry_shader="programs/tetrahedral_mesh/gen_tetra_geo.glsl",
            fragment_shader="programs/tetrahedral_mesh/lines_frag.glsl",
        )

        # Query object for measuring the rendering call in OpenGL
        # It delivers the GPU time it took to process commands
        self.query = self.ctx.query(samples=True, any_samples=True, time=True, primitives=True)
        self.total_elapsed = 0

    def render(self, time, frametime):

        # Render background
        self.ctx.wireframe = False
        if not self.with_blending:
            self.ctx.enable_only(moderngl.NOTHING)
            self.quad_fs.render(self.prog_background)

        # Handle blend mode toggle
        if self.with_blending:
            self.ctx.enable_only(moderngl.BLEND)
            self.ctx.blend_func = moderngl.ONE, moderngl.ONE
        else:
            self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        # Render tetrahedral mesh
        translate = glm.translate(glm.vec3(0.0, 2.5, -15.0))
        rotate = glm.mat4(glm.quat(glm.vec3(np.radians(180), 0, 0)))
        scale = glm.scale(glm.vec3(400, 400, 400))
        mat = self.camera.matrix * translate * rotate * scale

        # All render calls inside this context are timed
        with self.query:
            self.alive_texture.use(location=0)
            self.prog_gen_tetra["alive_texture"].value = 0
            self.prog_gen_tetra["threshold"].value = self.threshold
            self.prog_gen_tetra["color"].value = self.mesh_color
            self.prog_gen_tetra["m_cam"].write(mat)
            self.prog_gen_tetra["m_proj"].write(self.camera.projection.matrix)
            self.geometry.render(self.prog_gen_tetra, mode=moderngl.LINES_ADJACENCY)

            # Render lines
            self.ctx.wireframe = True
            self.alive_texture.use(location=0)
            self.prog_gen_tetra_lines["alive_texture"].value = 0
            self.prog_gen_tetra_lines["threshold"].value = self.threshold
            self.prog_gen_tetra_lines["color"].value = self.line_color
            self.prog_gen_tetra_lines["m_cam"].write(mat)
            self.prog_gen_tetra_lines["m_proj"].write(self.camera.projection.matrix)
            self.geometry.render(self.prog_gen_tetra_lines, mode=moderngl.LINES_ADJACENCY)

        self.total_elapsed = self.query.elapsed

    def key_event(self, key, action, modifiers):
        super().key_event(key, action, modifiers)
        keys = self.wnd.keys

        if action == keys.ACTION_PRESS:
            if key == keys.B:
                self.with_blending = not self.with_blending
                print("With blending:", self.with_blending)
                if self.with_blending:
                    self.mesh_color = 0.01, 0.01, 0.01
                    self.line_color = 0.01, 0.01, 0.01
                else:
                    self.mesh_color = 0.0, 0.8, 0.0
                    self.line_color = 0.0, 0.0, 0.0

    def mouse_scroll_event(self, x_offset, y_offset):
        if y_offset > 0:
            self.threshold += 0.01
        else:
            self.threshold -= 0.01

        self.threshold = max(min(self.threshold, 1.0), 0.0)

    def close(self):
        # 1 s = 1000000000 ns
        # 1 s = 1000000 μs
        avg = self.total_elapsed / self.wnd.frames
        print(
            "Average rendering time per frame: {} ns | {} μs".format(
                round(avg, 4),  # ns
                round(avg / 1000, 4),  # μs
            )
        )


if __name__ == "__main__":
    VolumetricTetrahedralMesh.run()
