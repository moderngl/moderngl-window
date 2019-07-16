from pathlib import Path
from pyrr import Matrix44, matrix44, Vector3

import moderngl
import moderngl_window as mglw
from moderngl_window import resources
from moderngl_window.meta import (
    SceneDescription,
)
from moderngl_window.scene.camera import KeyboardCamera

resources.register_dir((Path(__file__).parent / 'resources').resolve())
# Test models from: https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0
resources.register_dir(Path(__file__, '../../../glTF-Sample-Models/2.0').resolve())


class CubeModel(mglw.WindowConfig):
    # window_size = (1920, 1080)
    aspect_ratio = 16 / 9

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scene = resources.scenes.load(SceneDescription(path='scenes/crate.obj'))

        # --- glTF-Sample-Models ---
        # self.scene = resources.scenes.load(SceneDescription(path='2CylinderEngine/glTF-Binary/2CylinderEngine.glb'))
        # self.scene = resources.scenes.load(SceneDescription(path='CesiumMilkTruck/glTF-Embedded/CesiumMilkTruck.gltf'))
        # self.scene = resources.scenes.load(SceneDescription(path='CesiumMilkTruck/glTF-Binary/CesiumMilkTruck.glb'))
        # self.scene = resources.scenes.load(SceneDescription(path='CesiumMilkTruck/glTF/CesiumMilkTruck.gltf'))
        # self.scene = resources.scenes.load(SceneDescription(path='Sponza/glTF/Sponza.gltf'))
        # self.scene = resources.scenes.load(SceneDescription(path='Lantern/glTF-Binary/Lantern.glb'))
        # self.scene = resources.scenes.load(SceneDescription(path='Buggy/glTF-Binary/Buggy.glb'))
        # self.scene = resources.scenes.load(SceneDescription(path='VC/glTF-Binary/VC.glb'))
        # self.scene = resources.scenes.load(SceneDescription(path='DamagedHelmet/glTF-Binary/DamagedHelmet.glb'))

        self.camera = KeyboardCamera(self.wnd.keys, fov=75.0, aspect=self.wnd.aspect_ratio, near=0.1, far=1000.0)
        # Use this for gltf scenes for better camera controls
        if self.scene.diagonal_size > 0:
            self.camera.velocity = self.scene.diagonal_size / 5.0

    def render(self, time: float, frametime: float):
        """Render the scene"""
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
        # # Currently only works with GLFT
        # self.scene.draw_bbox(
        #     projection_matrix=self.camera.projection.matrix,
        #     camera_matrix=camera_matrix,
        #     children=True,
        # )

    def key_event(self, key, action, modifiers):
        self.camera.key_input(key, action, modifiers)

    def mouse_position_event(self, x: int, y: int):
        self.camera.rot_state(x, y)

    def resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)


if __name__ == '__main__':
    mglw.run_window_config(CubeModel)
