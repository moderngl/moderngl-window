"""
Based partly on BlubberQuark's blog:
https://blubberquark.tumblr.com/post/185013752945/using-moderngl-for-post-processing-shaders-with

Basic example showing how to efficiently render a pygame surface with moderngl
in the most efficient way. We include alpha channel as well since this
is a very common use case.

This involves to steps:
* Copy the surface data from system memory into graphics memory (texture)
* Render this texture to the screen with some simple geometry

There are two common ways to get the pixel data from a pygame surface:
* pygame.image.tostring(surface, "RGBA", ...)
* surface.get_view("1")

We're using get_view() here because it's faster and more efficient.
In fact about 700+ times faster than tostring() since get_view() doesn't
copy or transform the data in any way.
This however comes with a caveat:

* The raw data of the surface is in BGRA format instead of RGBA so
  we need to set a swizzle on the OpenGL texture to swap the channels.
  This just means OpenGL will swap the channels when reading the data.
  It's pretty much a "free" operation.
* OpenGL are storing textures upside down so we usually need to flip
  the texture. The raw surface data is not flipped, but we can flip
  the texture coordinates instead.

To be as explicit as possible we're not using any shortcuts and include
our own shader program and geometry to render the texture to the screen.
In other words: we are using none of the shortcuts in moderngl-window.

Also note that this example can easily be tweaked to only use RGB data
instead of RGBA if alpha channel is not needed.

Other notes:
* We don't use any projection in this example working directly in
  normalized device coordinates. Meaning we are working in the range
  [-1, 1] for both x and y.
* Texture coordinates are in the [0.0, 1.0] range.
"""

import math
from array import array

import pygame

import moderngl
import moderngl_window


class Pygame(moderngl_window.WindowConfig):
    """
    Example drawing a pygame surface with moderngl.
    """

    title = "Pygame"
    window_size = 1280, 720

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.wnd.name != "pygame2":
            raise RuntimeError("This example only works with --window pygame2 option")

        # The resolution of the pygame surface
        self.pg_res = 320, 180
        # Create a 24bit (rgba) offscreen surface pygame can render to
        self.pg_screen = pygame.Surface(self.pg_res, flags=pygame.SRCALPHA)
        # 32 bit (rgba) moderngl texture (4 channels, RGBA)
        self.pg_texture = self.ctx.texture(self.pg_res, 4)
        # Change the texture filtering to NEAREST for pixelated look.
        self.pg_texture.filter = moderngl.NEAREST, moderngl.NEAREST
        # The pygame surface is stored in BGRA format but RGBA
        # so we simply change the order of the channels of the texture
        self.pg_texture.swizzle = "BGRA"

        # Let's make a custom texture shader rendering the surface
        self.texture_program = self.ctx.program(
            vertex_shader="""
                #version 330
                // Vertex shader runs once for each vertex in the geometry

                in vec2 in_vert;
                in vec2 in_texcoord;
                out vec2 uv;

                void main() {
                    // Send the texture coordinates to the fragment shader
                    uv = in_texcoord;
                    // Resolve the vertex position
                    gl_Position = vec4(in_vert, 0.0, 1.0);
                }
            """,
            fragment_shader="""
                #version 330
                // Fragment shader runs once for each pixel in the triangles.
                // We are drawing two triangles here creating a quad.
                // In values are interpolated between the vertices.

                // Sampler reading from a texture channel 0
                uniform sampler2D surface;

                // The pixel we are writing to the screen
                out vec4 f_color;
                // Interpolated texture coordinates
                in vec2 uv;

                void main() {
                    // Simply look up the color from the texture
                    f_color = texture(surface, uv);
                }
            """,
        )
        # Explicitly configure the sampler to read from texture channel 0.
        # Most hardware today supports 8-16 different channels for multi-texturing.
        self.texture_program["surface"] = 0

        # Geometry to render the texture to the screen.
        # This is simply a "quad" covering the entire screen.
        # This is rendered as a triangle strip.
        # NOTE: using array.array is a simple way to create a buffer data
        # fmt: off
        buffer = self.ctx.buffer(
            data=array('f', [
                # Position (x, y) , Texture coordinates (x, y)
                -1.0, 1.0, 0.0, 1.0,  # upper left
                -1.0, -1.0, 0.0, 0.0,  # lower left
                1.0, 1.0, 1.0, 1.0,  # upper right
                1.0, -1.0, 1.0, 0.0,  # lower right
            ])
        )
        # fmt: on
        # Create a vertex array describing the buffer layout.
        # The shader program is also passed in there to sanity check
        # the attribute names.
        self.quad_fs = self.ctx.vertex_array(
            self.texture_program,
            [
                (
                    # The buffer containing the data
                    buffer,
                    # Format of the two attributes.
                    # - 2 floats for position
                    # - 2 floats for texture coordinates
                    "2f 2f",
                    # Names of the attributes in the shader program
                    "in_vert",
                    "in_texcoord",
                )
            ],
        )

    def render(self, time: float, frame_time: float):
        """Called every frame"""
        self.render_pygame(time)

        # Clear the screen
        self.ctx.clear(
            (math.sin(time) + 1.0) / 2,
            (math.sin(time + 2) + 1.0) / 2,
            (math.sin(time + 3) + 1.0) / 2,
        )

        # Enable blending for transparency
        self.ctx.enable(moderngl.BLEND)
        # Bind the texture to texture channel 0
        self.pg_texture.use(location=0)
        # Render the quad to the screen. Will use the texture we bound above.
        self.quad_fs.render(mode=moderngl.TRIANGLE_STRIP)
        # Disable blending
        self.ctx.disable(moderngl.BLEND)

    def render_pygame(self, time: float):
        """Render to offscreen surface and copy result into moderngl texture"""
        self.pg_screen.fill((0, 0, 0, 0))  # Make sure we clear with alpha 0!
        # Draw some simple circles to the surface
        N = 8
        for i in range(N):
            time_offset = 6.28 / N * i
            pygame.draw.circle(
                self.pg_screen,
                ((i * 50) % 255, (i * 100) % 255, (i * 20) % 255),
                (
                    math.sin(time + time_offset) * 55 + self.pg_res[0] // 2,
                    math.cos(time + time_offset) * 55 + self.pg_res[1] // 2,
                ),
                math.sin(time) * 4 + 15,
            )

        # Get the buffer view of the Surface's pixels
        # and write this data into the texture
        texture_data = self.pg_screen.get_view("1")
        self.pg_texture.write(texture_data)


if __name__ == "__main__":
    moderngl_window.run_window_config(Pygame, args=("--window", "pygame2"))
