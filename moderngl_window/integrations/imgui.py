import moderngl
import imgui
from imgui.integrations.opengl import ProgrammablePipelineRenderer
from imgui.integrations.opengl import BaseOpenGLRenderer


class ModernglWindowMixin:
    REVERSE_KEY_MAP = {}

    def resize(self, width: int, height: int):
        self.io.display_size = width, height

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if action == keys.ACTION_PRESS:
            if key in self.REVERSE_KEY_MAP:
                self.io.keys_down[self.REVERSE_KEY_MAP[key]] = True
        else:
            if key in self.REVERSE_KEY_MAP:
                self.io.keys_down[self.REVERSE_KEY_MAP[key]] = False

    def mouse_position_event(self, x, y, dx, dy):
        self.io.mouse_pos = x, y

    def mouse_drag_event(self, x, y, dx, dy):
        self.io.mouse_pos = x, y

        if self.wnd.mouse_states.left:
            self.io.mouse_down[0] = 1

        if self.wnd.mouse_states.middle:
            self.io.mouse_down[1] = 1

        if self.wnd.mouse_states.right:
            self.io.mouse_down[2] = 1

    def mouse_scroll_event(self, x_offset, y_offset):
        self.io.mouse_wheel = y_offset

    def mouse_press_event(self, x, y, button):
        self.io.mouse_pos = x, y

        if button == self.wnd.mouse.left:
            self.io.mouse_down[0] = 1

        if button == self.wnd.mouse.middle:
            self.io.mouse_down[1] = 1

        if button == self.wnd.mouse.right:
            self.io.mouse_down[2] = 1

    def mouse_release_event(self, x: int, y: int, button: int):
        self.io.mouse_pos = x, y

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
            Out_Color = Frag_Color * texture(Texture, Frag_UV.st);
        }
    """

    def __init__(self, *args, **kwargs):
        self._prog = None
        self._fbo = None
        self._font_texture = None
        self._vertex_buffer = None
        self._index_buffer = None
        self._vao = None
        self._scope = None
        self.ctx = kwargs.get('ctx')

        if not self.ctx:
            raise ValueError('Missing moderngl contex')

        super().__init__()

    def refresh_font_texture(self):
        print('refresh_font_texture')
        width, height, pixels = self.io.fonts.get_tex_data_as_rgba32()

        if self._font_texture:
            self._font_texture.release()

        self._font_texture = self.ctx.texture((width, height), 4, data=pixels)
        self.io.fonts.texture_id = self._font_texture.glo
        self.io.fonts.clear_tex_data()

    def _create_device_objects(self):
        print('_create_device_objects')
        self._prog = self.ctx.program(
            vertex_shader=self.VERTEX_SHADER_SRC,
            fragment_shader=self.FRAGMENT_SHADER_SRC,
        )
        self._vertex_buffer = self.ctx.buffer(reserve=imgui.VERTEX_SIZE * 65536)
        self._index_buffer = self.ctx.buffer(reserve=imgui.INDEX_SIZE * 65536)
        self._vao = self.ctx.vertex_array(
            self._prog,
            [
                (self._vertex_buffer, '2f 2f 4f', 'Position', 'UV', 'Color'),
            ],
            index_buffer=self._index_buffer,
            index_element_size=imgui.INDEX_SIZE,
        )

    def render(self, draw_data):
        io = self.io

        if not self._scope:
            self._scope = self.ctx.scope(
                enable_only=moderngl.BLEND,
                textures=[(self._font_texture, 0)],
            )

        display_width, display_height = io.display_size
        fb_width = int(display_width * io.display_fb_scale[0])
        fb_height = int(display_height * io.display_fb_scale[1])

        if fb_width == 0 or fb_height == 0:
            return

        draw_data.scale_clip_rects(*io.display_fb_scale)
        self.ctx.blend_equation = moderngl.FUNC_ADD

        for commands in draw_data.commands_lists:
            print("vertex_buffer", type(commands.vtx_buffer_data), commands.vtx_buffer_data)
            print("index_buffer", type(commands.idx_buffer_data), commands.idx_buffer_data)
            data = 

            for command in commands.commands:
                with self._scope:
                    self._vao.render(moderngl.TRIANGLES)

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


class ModernglWindowRenderer(ModernglRenderer, ModernglWindowMixin):

    def __init__(self, window):
        super().__init__(ctx=window.ctx)
        self.wnd = window

        self.io.display_size = self.wnd.size
        self.io.display_fb_scale = 1, 1


class ModernglWindowRenderer2(ModernglWindowMixin, ProgrammablePipelineRenderer):

    def __init__(self, window):
        super().__init__()
        self.wnd = window

        self.io.display_size = self.wnd.size
        self.io.display_fb_scale = 1, 1
