import ctypes

import moderngl
from imgui_bundle import imgui
from imgui_bundle.python_backends import compute_fb_scale


class ModernglWindowMixin:
    io: imgui.IO

    def resize(self, width: int, height: int):
        self.io.display_size = self.wnd.size
        self.io.display_framebuffer_scale = compute_fb_scale(self.wnd.size, self.wnd.buffer_size)

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if key in self.REVERSE_KEYMAP:
            down = action == keys.ACTION_PRESS
            self.io.add_key_event(self.REVERSE_KEYMAP[key], down=down)

    def _mouse_pos_viewport(self, x, y):
        """Make sure mouse coordinates are correct with black borders"""
        return (
            int(x - (self.wnd.width - self.wnd.viewport_width / self.wnd.pixel_ratio) / 2),
            int(y - (self.wnd.height - self.wnd.viewport_height / self.wnd.pixel_ratio) / 2),
        )

    def mouse_position_event(self, x, y, dx, dy):
        self.io.mouse_pos = self._mouse_pos_viewport(x, y)

    def mouse_drag_event(self, x, y, dx, dy):
        self.io.mouse_pos = self._mouse_pos_viewport(x, y)

        if self.wnd.mouse_states.left:
            self.io.mouse_down[0] = 1

        if self.wnd.mouse_states.middle:
            self.io.mouse_down[2] = 1

        if self.wnd.mouse_states.right:
            self.io.mouse_down[1] = 1

    def mouse_scroll_event(self, x_offset, y_offset):
        self.io.mouse_wheel = y_offset

    def mouse_press_event(self, x, y, button):
        self.io.mouse_pos = self._mouse_pos_viewport(x, y)

        if button == self.wnd.mouse.left:
            self.io.mouse_down[0] = 1

        if button == self.wnd.mouse.middle:
            self.io.mouse_down[2] = 1

        if button == self.wnd.mouse.right:
            self.io.mouse_down[1] = 1

    def mouse_release_event(self, x: int, y: int, button: int):
        self.io.mouse_pos = self._mouse_pos_viewport(x, y)

        if button == self.wnd.mouse.left:
            self.io.mouse_down[0] = 0

        if button == self.wnd.mouse.middle:
            self.io.mouse_down[2] = 0

        if button == self.wnd.mouse.right:
            self.io.mouse_down[1] = 0

    def unicode_char_entered(self, char):
        io = imgui.get_io()
        io.add_input_character(ord(char))


class BaseOpenGLRenderer(object):
    def __init__(self):
        if not imgui.get_current_context():
            raise RuntimeError(
                "No valid ImGui context. Use imgui.create_context() first and/or "
                "imgui.set_current_context()."
            )
        self.io = imgui.get_io()

        self._font_texture = None

        self.io.delta_time = 1.0 / 60.0

        self._create_device_objects()
        self.refresh_font_texture()

    def render(self, draw_data):
        raise NotImplementedError

    def refresh_font_texture(self):
        raise NotImplementedError

    def _create_device_objects(self):
        raise NotImplementedError

    def _invalidate_device_objects(self):
        raise NotImplementedError

    def shutdown(self):
        self._invalidate_device_objects()


class ModernGLRenderer(BaseOpenGLRenderer):
    VERTEX_SHADER_SRC = """
        #version 330
        uniform mat4 ProjMtx;
        in vec2 Position;
        in vec2 UV;
        in vec4 Color;
        out vec2 Frag_UV;
        out vec4 Frag_Color;
        void main() {
            Frag_UV = UV;
            Frag_Color = Color;
            gl_Position = ProjMtx * vec4(Position.xy, 0, 1);
        }
    """
    FRAGMENT_SHADER_SRC = """
        #version 330
        uniform sampler2D Texture;
        in vec2 Frag_UV;
        in vec4 Frag_Color;
        out vec4 Out_Color;
        void main() {
            Out_Color = (Frag_Color * texture(Texture, Frag_UV.st));
        }
    """

    def __init__(self, *args, **kwargs):
        self._prog = None
        self._fbo = None
        self._font_texture = None
        self._vertex_buffer = None
        self._index_buffer = None
        self._vao = None
        self._textures = {}
        self.wnd = kwargs.get("wnd")
        self.ctx: moderngl.Context = (
            self.wnd.ctx if self.wnd and self.wnd.ctx else kwargs.get("ctx")
        )

        if not self.ctx:
            raise RuntimeError("Missing moderngl context")

        super().__init__()

        if hasattr(self, "wnd") and self.wnd:
            self.resize(*self.wnd.buffer_size)
        elif "display_size" in kwargs:
            self.io.display_size = kwargs.get("display_size")

    def register_texture(self, texture: moderngl.Texture):
        """Make the imgui renderer aware of the texture"""
        self._textures[texture.glo] = texture

    def remove_texture(self, texture: moderngl.Texture):
        """Remove the texture from the imgui renderer"""
        del self._textures[texture.glo]

    def refresh_font_texture(self):
        font_matrix = self.io.fonts.get_tex_data_as_rgba32()
        width = font_matrix.shape[1]
        height = font_matrix.shape[0]
        pixels = font_matrix.data

        if self._font_texture:
            self.remove_texture(self._font_texture)
            self._font_texture.release()

        self._font_texture = self.ctx.texture((width, height), 4, data=pixels)
        self.register_texture(self._font_texture)
        self.io.fonts.tex_id = self._font_texture.glo
        self.io.fonts.clear_tex_data()

    def _create_device_objects(self):
        self._prog = self.ctx.program(
            vertex_shader=self.VERTEX_SHADER_SRC,
            fragment_shader=self.FRAGMENT_SHADER_SRC,
        )
        self.projMat = self._prog["ProjMtx"]
        self._prog["Texture"].value = 0
        self._vertex_buffer = self.ctx.buffer(reserve=imgui.VERTEX_SIZE * 65536)
        self._index_buffer = self.ctx.buffer(reserve=imgui.INDEX_SIZE * 65536)
        self._vao = self.ctx.vertex_array(
            self._prog,
            [(self._vertex_buffer, "2f 2f 4f1", "Position", "UV", "Color")],
            index_buffer=self._index_buffer,
            index_element_size=imgui.INDEX_SIZE,
        )

    def render(self, draw_data: imgui.ImDrawData):
        io = self.io
        display_width, display_height = io.display_size
        fb_width = int(display_width * io.display_framebuffer_scale[0])
        fb_height = int(display_height * io.display_framebuffer_scale[1])

        if fb_width == 0 or fb_height == 0:
            return

        self.projMat.value = (
            2.0 / display_width,
            0.0,
            0.0,
            0.0,
            0.0,
            2.0 / -display_height,
            0.0,
            0.0,
            0.0,
            0.0,
            -1.0,
            0.0,
            -1.0,
            1.0,
            0.0,
            1.0,
        )

        draw_data.scale_clip_rects(imgui.ImVec2(*io.display_framebuffer_scale))

        self.ctx.enable_only(moderngl.BLEND)
        self.ctx.blend_equation = moderngl.FUNC_ADD
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA

        self._font_texture.use()

        for commands in draw_data.cmd_lists:
            # Write the vertex and index buffer data without copying it
            vtx_type = ctypes.c_byte * commands.vtx_buffer.size() * imgui.VERTEX_SIZE
            idx_type = ctypes.c_byte * commands.idx_buffer.size() * imgui.INDEX_SIZE
            vtx_arr = (vtx_type).from_address(commands.vtx_buffer.data_address())
            idx_arr = (idx_type).from_address(commands.idx_buffer.data_address())
            self._vertex_buffer.write(vtx_arr)
            self._index_buffer.write(idx_arr)

            idx_pos = 0
            for command in commands.cmd_buffer:
                texture = self._textures.get(command.texture_id)
                if texture is None:
                    raise ValueError(
                        (
                            "Texture {} is not registered. Please add to renderer using "
                            "register_texture(..). "
                            "Current textures: {}".format(command.texture_id, list(self._textures))
                        )
                    )

                texture.use(0)

                x, y, z, w = command.clip_rect
                self.ctx.scissor = int(x), int(fb_height - w), int(z - x), int(w - y)
                self._vao.render(moderngl.TRIANGLES, vertices=command.elem_count, first=idx_pos)
                idx_pos += command.elem_count

        self.ctx.scissor = None

    def _invalidate_device_objects(self):
        if self._font_texture:
            self._font_texture.release()
        if self._vertex_buffer:
            self._vertex_buffer.release()
        if self._index_buffer:
            self._index_buffer.release()
        if self._vao:
            self._vao.release()
        if self._prog:
            self._prog.release()

        self.io.fonts.tex_id = 0
        self._font_texture = None


class ModernglWindowRenderer(ModernGLRenderer, ModernglWindowMixin):
    def __init__(self, window):
        super().__init__(wnd=window)
        self.wnd = window

        self._init_key_maps()
        self.io.display_size = self.wnd.size
        self.io.display_framebuffer_scale = self.wnd.pixel_ratio, self.wnd.pixel_ratio

    def _init_key_maps(self):
        keys = self.wnd.keys

        self.REVERSE_KEYMAP = {
            keys.TAB: imgui.Key.tab,
            keys.LEFT: imgui.Key.left_arrow,
            keys.RIGHT: imgui.Key.right_arrow,
            keys.UP: imgui.Key.up_arrow,
            keys.DOWN: imgui.Key.down_arrow,
            keys.PAGE_UP: imgui.Key.page_up,
            keys.PAGE_DOWN: imgui.Key.page_down,
            keys.HOME: imgui.Key.home,
            keys.END: imgui.Key.end,
            keys.DELETE: imgui.Key.delete,
            keys.SPACE: imgui.Key.space,
            keys.BACKSPACE: imgui.Key.backspace,
            keys.ENTER: imgui.Key.enter,
            keys.ESCAPE: imgui.Key.escape,
        }
