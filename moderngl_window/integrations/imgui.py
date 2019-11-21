import ctypes

import numpy as np
import moderngl
import imgui
from imgui.integrations.opengl import ProgrammablePipelineRenderer
from imgui.integrations.opengl import BaseOpenGLRenderer


class ModernglWindowMixin:
    REVERSE_KEY_MAP = {}

    def resize(self, width: int, height: int):
        self.io.display_size = self.wnd.viewport_size

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if action == keys.ACTION_PRESS:
            if key in self.REVERSE_KEY_MAP:
                self.io.keys_down[self.REVERSE_KEY_MAP[key]] = True
        else:
            if key in self.REVERSE_KEY_MAP:
                self.io.keys_down[self.REVERSE_KEY_MAP[key]] = False

    def _mouse_pos_viewport(self, x, y):
        """Make sure mouse coordinates are correct with black borders"""
        return (
            x - (self.wnd.buffer_width - self.wnd.viewport_size[0]) // 2,
            y - (self.wnd.buffer_height - self.wnd.viewport_size[1]) // 2,
        )

    def mouse_position_event(self, x, y, dx, dy):
        self.io.mouse_pos = self._mouse_pos_viewport(x, y)

    def mouse_drag_event(self, x, y, dx, dy):
        self.io.mouse_pos = self._mouse_pos_viewport(x, y)

        if self.wnd.mouse_states.left:
            self.io.mouse_down[0] = 1

        if self.wnd.mouse_states.middle:
            self.io.mouse_down[1] = 1

        if self.wnd.mouse_states.right:
            self.io.mouse_down[2] = 1

    def mouse_scroll_event(self, x_offset, y_offset):
        self.io.mouse_wheel = y_offset

    def mouse_press_event(self, x, y, button):
        self.io.mouse_pos = self._mouse_pos_viewport(x, y)

        if button == self.wnd.mouse.left:
            self.io.mouse_down[0] = 1

        if button == self.wnd.mouse.middle:
            self.io.mouse_down[1] = 1

        if button == self.wnd.mouse.right:
            self.io.mouse_down[2] = 1

    def mouse_release_event(self, x: int, y: int, button: int):
        self.io.mouse_pos = self._mouse_pos_viewport(x, y)

        if button == self.wnd.mouse.left:
            self.io.mouse_down[0] = 0

        if button == self.wnd.mouse.middle:
            self.io.mouse_down[1] = 0

        if button == self.wnd.mouse.right:
            self.io.mouse_down[2] = 0

    def unicode_char_entered(self, char):
        io = imgui.get_io()

        for c in char:
            io.add_input_character(ord(c))


class ModernglRenderer(BaseOpenGLRenderer):

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
        self.ctx = kwargs.get('ctx')

        if not self.ctx:
            raise ValueError('Missing moderngl contex')

        super().__init__()

    def refresh_font_texture(self):
        width, height, pixels = self.io.fonts.get_tex_data_as_rgba32()

        if self._font_texture:
            self._font_texture.release()

        self._font_texture = self.ctx.texture((width, height), 4, data=pixels)
        self.io.fonts.texture_id = self._font_texture.glo
        self.io.fonts.clear_tex_data()

    def _create_device_objects(self):
        self._prog = self.ctx.program(
            vertex_shader=self.VERTEX_SHADER_SRC,
            fragment_shader=self.FRAGMENT_SHADER_SRC,
        )
        self.projMat = self._prog['ProjMtx']
        self._prog['Texture'].value = 0
        self._vertex_buffer = self.ctx.buffer(reserve=imgui.VERTEX_SIZE * 65536)
        self._index_buffer = self.ctx.buffer(reserve=imgui.INDEX_SIZE * 65536)
        self._vao = self.ctx.vertex_array(
            self._prog,
            [
                (self._vertex_buffer, '2f 2f 4f1', 'Position', 'UV', 'Color'),
            ],
            index_buffer=self._index_buffer,
            index_element_size=imgui.INDEX_SIZE,
        )

    def render(self, draw_data):
        io = self.io

        display_width, display_height = io.display_size
        fb_width = int(display_width * io.display_fb_scale[0])
        fb_height = int(display_height * io.display_fb_scale[1])

        if fb_width == 0 or fb_height == 0:
            return

        self.projMat.value = (
            2.0 / display_width, 0.0, 0.0, 0.0,
            0.0, 2.0 / -display_height, 0.0, 0.0,
            0.0, 0.0, -1.0, 0.0,
            -1.0, 1.0, 0.0, 1.0,
        )

        draw_data.scale_clip_rects(*io.display_fb_scale)

        self.ctx.enable_only(moderngl.BLEND)
        self.ctx.blend_equation = moderngl.FUNC_ADD
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA

        self._font_texture.use()

        for commands in draw_data.commands_lists:
            # Create a numpy array mapping the vertex and index buffer data without copying it
            vtx_ptr = ctypes.cast(commands.vtx_buffer_data, ctypes.POINTER(ctypes.c_byte))
            idx_ptr = ctypes.cast(commands.idx_buffer_data, ctypes.POINTER(ctypes.c_byte))
            vtx_data = np.ctypeslib.as_array(vtx_ptr, (commands.vtx_buffer_size * imgui.VERTEX_SIZE,))
            idx_data = np.ctypeslib.as_array(idx_ptr, (commands.idx_buffer_size * imgui.INDEX_SIZE,))
            self._vertex_buffer.write(vtx_data)
            self._index_buffer.write(idx_data)

            idx_pos = 0
            for command in commands.commands:
                x, y, z, w = command.clip_rect
                # self.ctx.scissor = int(x), int(fb_height - w), int(z - x), int(w - y)
                self._vao.render(moderngl.TRIANGLES, vertices=command.elem_count, first=idx_pos)
                idx_pos += command.elem_count

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

        self.io.fonts.texture_id = 0
        self._font_texture = None


class ModernglWindowRenderer(ModernglRenderer, ModernglWindowMixin):

    def __init__(self, window):
        super().__init__(ctx=window.ctx)
        self.wnd = window

        self.io.display_size = self.wnd.size
        scale = self.wnd.buffer_size[0] / self.wnd.size[0]
        self.io.display_fb_scale = scale, scale


class ModernglWindowRenderer2(ModernglWindowMixin, ProgrammablePipelineRenderer):

    def __init__(self, window):
        super().__init__()
        self.wnd = window

        self.io.display_size = self.wnd.size
        self.io.display_fb_scale = 1.0, 1.0
