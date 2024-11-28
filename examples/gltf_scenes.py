from pathlib import Path

import glm
import moderngl
from base import CameraWindow

import moderngl_window as mglw
from moderngl_window.scene.camera import KeyboardCamera


class CubeModel(CameraWindow):
    """
    In oder for this example to work you need to clone the gltf
    model samples repository and ensure resource_dir is set correctly:
    https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0
    """

    title = "GL Transmission Format (glTF) 2.0 Scene"
    window_size = 1280, 720
    aspect_ratio = None
    resource_dir = Path(__file__, "../../../glTF-Sample-Models/2.0").resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True

        # --- glTF-Sample-Models ---
        # self.scene = self.load_scene("2CylinderEngine/glTF-Binary/2CylinderEngine.glb")
        # self.scene = self.load_scene('CesiumMilkTruck/glTF-Embedded/CesiumMilkTruck.gltf')
        # self.scene = self.load_scene("CesiumMilkTruck/glTF-Binary/CesiumMilkTruck.glb")
        # self.scene = self.load_scene("CesiumMilkTruck/glTF/CesiumMilkTruck.gltf")
        # self.scene = self.load_scene("Sponza/glTF/Sponza.gltf")
        # self.scene = self.load_scene("Lantern/glTF-Binary/Lantern.glb")
        # self.scene = self.load_scene("Buggy/glTF-Binary/Buggy.glb")
        self.scene = self.load_scene("VC/glTF-Binary/VC.glb")
        # self.scene = self.load_scene('DamagedHelmet/glTF-Binary/DamagedHelmet.glb')
        # self.scene = self.load_scene("BoxInterleaved/glTF/BoxInterleaved.gltf")
        # self.scene = self.load_scene("OrientationTest/glTF/OrientationTest.gltf")
        # self.scene = self.load_scene("AntiqueCamera/glTF/AntiqueCamera.gltf")
        # self.scene = self.load_scene("BoomBox/glTF/BoomBox.gltf")
        # self.scene = self.load_scene('Box/glTF/Box.gltf')
        # self.scene = self.load_scene("BoxTextured/glTF/BoxTextured.gltf")
        # self.scene = self.load_scene(
        #     "BoxTexturedNonPowerOfTwo/glTF/BoxTexturedNonPowerOfTwo.gltf"
        # )
        # self.scene = self.load_scene("BoxVertexColors/glTF/BoxVertexColors.gltf")
        # self.scene = self.load_scene("BrainStem/glTF/BrainStem.gltf")
        # self.scene = self.load_scene("Corset/glTF/Corset.gltf")
        # self.scene = self.load_scene("FlightHelmet/glTF/FlightHelmet.gltf")
        # self.scene = self.load_scene("Fox/glTF/Fox.gltf")
        # self.scene = self.load_scene("GearboxAssy/glTF/GearboxAssy.gltf")
        # self.scene = self.load_scene("ReciprocatingSaw/glTF/ReciprocatingSaw.gltf")
        # self.scene = self.load_scene('RiggedFigure/glTF/RiggedFigure.gltf')
        # self.scene = self.load_scene("RiggedSimple/glTF/RiggedSimple.gltf")
        # self.scene = self.load_scene("SciFiHelmet/glTF/SciFiHelmet.gltf")
        # self.scene = self.load_scene("SimpleMeshes/glTF/SimpleMeshes.gltf")
        # self.scene = self.load_scene(
        #     "SimpleSparseAccessor/glTF/SimpleSparseAccessor.gltf"
        # )
        # self.scene = self.load_scene("Suzanne/glTF/Suzanne.gltf")
        # self.scene = self.load_scene(
        #     "TextureCoordinateTest/glTF/TextureCoordinateTest.gltf"
        # )
        # self.scene = self.load_scene(
        #     "TextureSettingsTest/glTF/TextureSettingsTest.gltf"
        # )
        # self.scene = self.load_scene("VertexColorTest/glTF/VertexColorTest.gltf")
        # self.scene = self.load_scene("WaterBottle/glTF/WaterBottle.gltf")

        self.camera = KeyboardCamera(
            self.wnd.keys,
            fov=75.0,
            aspect_ratio=self.wnd.aspect_ratio,
            near=0.1,
            far=1000.0,
        )
        self.camera.velocity = 10.0
        self.camera.mouse_sensitivity = 0.25

        # Use this for gltf scenes for better camera controls
        # if self.scene.diagonal_size > 0:
        #     self.camera.velocity = self.scene.diagonal_size / 5.0

    def on_render(self, time: float, frame_time: float):
        """Render the scene"""
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        # Move camera in on the z axis slightly by default
        translation = glm.translate(glm.vec3(0, 0, -1.5))
        camera_matrix = self.camera.matrix * translation

        self.scene.draw(
            projection_matrix=self.camera.projection.matrix,
            camera_matrix=camera_matrix,
            time=time,
        )

        # Draw bounding boxes
        self.scene.draw_bbox(
            projection_matrix=self.camera.projection.matrix,
            camera_matrix=camera_matrix,
            children=True,
            color=(0.75, 0.75, 0.75),
        )

        # self.scene.draw_wireframe(
        #     projection_matrix=self.camera.projection.matrix,
        #     camera_matrix=camera_matrix,
        #     color=(1, 1, 1, 1),
        # )


if __name__ == "__main__":
    mglw.run_window_config(CubeModel)
