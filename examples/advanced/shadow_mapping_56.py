"""
Shadow mapping example from:
https://www.opengl-tutorial.org/intermediate-tutorials/tutorial-16-shadow-mapping/
"""

import math
from pathlib import Path

import glm
import moderngl
from base import CameraWindow

import moderngl_window
from moderngl_window import geometry


class ShadowMapping(CameraWindow):
    title = "Shadow Mapping"
    resource_dir = (Path(__file__) / "../../resources").resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.projection.update(near=1, far=200)
        self.wnd.mouse_exclusivity = True

        # Offscreen buffer
        offscreen_size = 1024, 1024
        self.offscreen_depth = self.ctx.depth_texture(offscreen_size)
        self.offscreen_depth.compare_func = ""
        self.offscreen_depth.repeat_x = False
        self.offscreen_depth.repeat_y = False
        # Less ugly by default with linear. May need to be NEAREST for some techniques
        self.offscreen_depth.filter = moderngl.LINEAR, moderngl.LINEAR

        self.offscreen = self.ctx.framebuffer(
            depth_attachment=self.offscreen_depth,
        )

        # Scene geometry
        self.floor = geometry.cube(size=(25.0, 1.0, 25.0))
        self.wall = geometry.cube(size=(1.0, 5, 25), center=(-12.5, 2, 0))
        self.sphere = geometry.sphere(radius=5.0, sectors=64, rings=32)
        self.sun = geometry.sphere(radius=1.0)

        # Debug geometry
        self.offscreen_quad = geometry.quad_2d(size=(0.5, 0.5), pos=(0.75, 0.75))
        self.offscreen_quad2 = geometry.quad_2d(size=(0.5, 0.5), pos=(0.25, 0.75))

        # Programs
        self.raw_depth_prog = self.load_program(
            "programs/shadow_mapping/raw_depth.glsl"
        )
        self.basic_light = self.load_program(
            "programs/shadow_mapping/directional_light.glsl"
        )
        self.basic_light["shadowMap"].value = 0
        self.basic_light["color"].value = 1.0, 1.0, 1.0, 1.0
        self.shadowmap_program = self.load_program(
            "programs/shadow_mapping/shadowmap.glsl"
        )
        self.texture_prog = self.load_program("programs/texture.glsl")
        self.texture_prog["texture0"].value = 0
        self.sun_prog = self.load_program("programs/cube_simple.glsl")
        self.sun_prog["color"].value = 1, 1, 0, 1
        self.lightpos = 0, 0, 0

    def render(self, time, frametime):
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.lightpos = glm.vec3(math.sin(time) * 20, 5, math.cos(time) * 20)
        scene_pos = glm.vec3(0, -5, -32)

        # --- PASS 1: Render shadow map
        self.offscreen.clear()
        self.offscreen.use()

        depth_projection = glm.ortho(-20, 20, -20, 20, -20, 40)
        depth_view = glm.lookAt(self.lightpos, (0, 0, 0), (0, 1, 0))
        depth_mvp = depth_projection * depth_view
        self.shadowmap_program["mvp"].write(depth_mvp)

        self.floor.render(self.shadowmap_program)
        self.wall.render(self.shadowmap_program)
        self.sphere.render(self.shadowmap_program)

        # --- PASS 2: Render scene to screen
        self.wnd.use()
        self.basic_light["m_proj"].write(self.camera.projection.matrix)
        self.basic_light["m_camera"].write(self.camera.matrix)
        self.basic_light["m_model"].write(glm.translate(glm.vec3(scene_pos)))
        bias_matrix = glm.mat4(
            [
                [0.5, 0.0, 0.0, 0.0],
                [0.0, 0.5, 0.0, 0.0],
                [0.0, 0.0, 0.5, 0.0],
                [0.5, 0.5, 0.5, 1.0],
            ],
        )
        self.basic_light["m_shadow_bias"].write(bias_matrix * depth_mvp)
        self.basic_light["lightDir"].write(self.lightpos)
        self.offscreen_depth.use(location=0)
        self.floor.render(self.basic_light)
        self.wall.render(self.basic_light)
        self.sphere.render(self.basic_light)

        # Render the sun position
        self.sun_prog["m_proj"].write(self.camera.projection.matrix)
        self.sun_prog["m_camera"].write(self.camera.matrix)
        self.sun_prog["m_model"].write(
            glm.translate(glm.vec3(self.lightpos + scene_pos))
        )
        self.sun.render(self.sun_prog)

        # --- PASS 3: Debug ---
        # self.ctx.enable_only(moderngl.NOTHING)
        self.offscreen_depth.use(location=0)
        self.offscreen_quad.render(self.raw_depth_prog)
        # self.offscreen_color.use(location=0)
        # self.offscreen_quad2.render(self.texture_prog)


if __name__ == "__main__":
    moderngl_window.run_window_config(ShadowMapping)
