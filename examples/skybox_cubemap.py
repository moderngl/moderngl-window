from pathlib import Path
import moderngl
import moderngl_window
from moderngl_window import geometry
from base import CameraWindow


class Cubemap(CameraWindow):
    """Example loading and rendering a cubemap"""
    title = "Skybox with cubemap"
    resource_dir = (Path(__file__).parent / 'resources').resolve()
    aspect_ratio = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.cube = geometry.cube(size=(20, 20, 20))
        self.texture = self.load_texture_cube(
            neg_x='textures/cubemaps/yokohama/posx.jpg',
            neg_y='textures/cubemaps/yokohama/negy.jpg',
            neg_z='textures/cubemaps/yokohama/negz.jpg',
            pos_x='textures/cubemaps/yokohama/negx.jpg',
            pos_y='textures/cubemaps/yokohama/posy.jpg',
            pos_z='textures/cubemaps/yokohama/posz.jpg',
            flip_x=True,
        )
        self.prog = self.load_program('programs/cubemap.glsl')

    def render(self, time, frame_time):
        self.ctx.enable_only(moderngl.CULL_FACE)
        self.ctx.front_face = 'cw'

        cam = self.camera.matrix
        # Purge camera translation
        cam[3][0] = 0
        cam[3][1] = 0
        cam[3][2] = 0

        self.texture.use(location=0)
        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_camera'].write(cam)

        self.cube.render(self.prog)


if __name__ == '__main__':
    moderngl_window.run_window_config(Cubemap)
