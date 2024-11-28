from pathlib import Path

import moderngl
from base import OrbitCameraWindow


class OrbitCamCrate(OrbitCameraWindow):
    """
    Example showing how to use a OrbitCamera
    """

    aspect_ratio = 16 / 9
    resource_dir = Path(__file__).parent.resolve() / "resources"
    title = "Crate.obj Model - Orbit Camera"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True

        self.scene = self.load_scene("scenes/crate.obj")

        self.camera.projection.update(near=0.1, far=100.0)
        self.camera.mouse_sensitivity = 0.75
        self.camera.zoom = 2.5

    def on_render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        self.scene.draw(
            projection_matrix=self.camera.projection.matrix,
            camera_matrix=self.camera.matrix,
            time=time,
        )


if __name__ == "__main__":
    OrbitCamCrate.run()
