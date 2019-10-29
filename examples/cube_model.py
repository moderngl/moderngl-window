from pathlib import Path
from pyrr import Matrix44, matrix44, Vector3

import moderngl
import moderngl_window as mglw
from base import CameraWindow


class CubeModel(CameraWindow):
    # window_size = (1920, 1080)
    aspect_ratio = 16 / 9
    resource_dir = Path(__file__).parent.resolve() / 'resources'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True

        self.scene = self.load_scene('scenes/crate.obj')
        # self.scene = self.load_scene('scenes/Apollo_17.stl')

        self.camera.projection.update(near=0.1, far=100.0)
        self.camera.velocity = 7.0
        self.camera.mouse_sensitivity = 0.3

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        # Create camera matrix with rotation and translation
        translation = matrix44.create_from_translation((0, 0, -1.5))
        # rotation = matrix44.create_from_eulers((time, time, time))
        rotation = matrix44.create_from_eulers((0, 0, 0))
        model_matrix = matrix44.multiply(rotation, translation)

        camera_matrix = matrix44.multiply(model_matrix, self.camera.matrix)

        self.scene.draw(
            projection_matrix=self.camera.projection.matrix,
            camera_matrix=camera_matrix,
            time=time,
        )


if __name__ == '__main__':
    mglw.run_window_config(CubeModel)
