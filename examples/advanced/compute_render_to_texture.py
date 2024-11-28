from pathlib import Path

import moderngl as mgl

import moderngl_window as mglw
from moderngl_window import geometry


class ComputeRenderToTexture(mglw.WindowConfig):
    """Simple example rendering to a texture with a compute shader"""

    title = "Render Texture Using Compute Shader"
    resource_dir = (Path(__file__) / "../../resources").resolve()
    gl_version = 4, 3
    aspect_ratio = 1.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.compute_shader = self.load_compute_shader("programs/compute/render_to_texture.glsl")
        self.compute_shader["destTex"] = 0
        self.texture_program = self.load_program("programs/texture.glsl")
        self.quad_fs = geometry.quad_fs()
        self.texture = self.ctx.texture((256, 256), 4)
        self.texture.filter = mgl.NEAREST, mgl.NEAREST

    def on_render(self, time, frame_time):
        self.ctx.clear(0.3, 0.3, 0.3)

        w, h = self.texture.size
        gw, gh = 16, 16
        nx, ny, nz = int(w / gw), int(h / gh), 1

        try:
            self.compute_shader["time"] = time
        except Exception:
            pass
        # Automatically binds as a GL_R32F / r32f (read from the texture)
        self.texture.bind_to_image(0, read=False, write=True)
        self.compute_shader.run(nx, ny, nz)

        # Render texture
        self.texture.use(location=0)
        self.quad_fs.render(self.texture_program)


if __name__ == "__main__":
    ComputeRenderToTexture.run()
