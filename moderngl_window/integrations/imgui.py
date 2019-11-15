import imgui
# from imgui.integrations.opengl import ProgrammablePipelineRenderer
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
        self._ctx = kwargs.get('ctx')

        if not self._ctx:
            raise ValueError('Missing moderngl contex')

        super().__init__()

    def refresh_font_texture(self):
        width, height, pixels = self.io.fonts.get_tex_data_as_rgba32()

        if self._font_texture:
            self._font_texture.release()

        self._ctx.texture((width, height), 4, data=pixels)
        self.io.fonts.texture_id = self._font_texture.glo
        self.io.fonts.clear_tex_data()

    def _create_device_objects(self):
        self._prog = self.ctx.program(
            vertex_shader=self.VERTEX_SHADER_SRC,
            fragment_shader=self.FRAGMENT_SHADER_SRC,
        )


class ModernglWindowRenderer(ModernglRenderer, ModernglWindowMixin):

    def __init__(self, window):
        super().__init__(ctx=window.ctx)
        self.wnd = window

        self.io.display_size = self.wnd.size
        self.io.display_fb_scale = 1, 1
