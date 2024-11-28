from pathlib import Path

import glm
import moderngl
from base import CameraWindow

import moderngl_window


class CubeModel(CameraWindow):
    aspect_ratio = 16 / 9
    resource_dir = Path(__file__).parent.resolve() / "resources"
    title = "Cube Model"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True

        self.scene = self.load_scene("scenes/crate.obj")
        # self.scene = self.load_scene('scenes/Apollo_17.stl')

        self.camera.projection.update(near=0.1, far=100.0)
        self.camera.velocity = 7.0
        self.camera.mouse_sensitivity = 0.3

    def on_render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        translation = glm.translate(glm.vec3(0, 0, -1.5))
        rotation = glm.mat4(glm.quat(glm.vec3(0, 0, 0)))
        model_matrix = translation * rotation
        camera_matrix = self.camera.matrix * model_matrix

        self.scene.draw(
            projection_matrix=self.camera.projection.matrix,
            camera_matrix=camera_matrix,
            time=time,
        )


if __name__ == "__main__":
    moderngl_window.run_window_config(CubeModel)
