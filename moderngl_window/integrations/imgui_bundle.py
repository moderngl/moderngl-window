import ctypes

import moderngl
from imgui_bundle import imgui
from imgui_bundle.python_backends import compute_fb_scale


def _log_texture(msg: str):
    pass
    # import logging
    # logging.warning(msg)


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
        self.io.mouse_wheel_h = x_offset
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


class ModernGLRenderer:
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
        self._vertex_buffer = None
        self._index_buffer = None
        self._vao = None
        self._textures: dict[int, moderngl.Texture] = {}

        self.wnd = kwargs.get("wnd")
        self.ctx: moderngl.Context = (
            self.wnd.ctx if self.wnd and self.wnd.ctx else kwargs.get("ctx")
        )

        if not self.ctx:
            raise RuntimeError("Missing moderngl context")

        # Create base ImGui device objects (shaders, buffers)
        self._create_device_objects()

        # Basic IO setup
        self.io = imgui.get_io()
        self.io.delta_time = 1.0 / 60.0

        # Honor ImGui v1.92 RendererHasTextures
        io = imgui.get_io()
        io.backend_flags |= imgui.BackendFlags_.renderer_has_textures.value
        max_texture_size = self.ctx.info["GL_MAX_TEXTURE_SIZE"]
        pio = imgui.get_platform_io()
        pio.renderer_texture_max_width = max_texture_size
        pio.renderer_texture_max_height = max_texture_size

        if hasattr(self, "wnd") and self.wnd:
            self.resize(*self.wnd.buffer_size)
        elif "display_size" in kwargs:
            self.io.display_size = kwargs.get("display_size")

    # -------------------------------------------------------------------------
    # --- ImGui v1.92 Texture Lifecycle ---------------------------------------
    # -------------------------------------------------------------------------

    def _update_textures(self) -> None:
        """Sync ImGui texture registry with backend."""
        for tex in imgui.get_platform_io().textures:
            if tex.status != imgui.ImTextureStatus.ok:
                self._update_texture(tex)

    def _destroy_all_textures(self) -> None:
        """Force-destroy all ImGui-managed textures."""
        for t in list(imgui.get_platform_io().textures):
            if t.ref_count <= 1:
                t.status = imgui.ImTextureStatus.want_destroy
                self._update_texture(t)

    def _update_texture(self, tex: imgui.ImTextureData) -> None:
        """Handle texture creation, update, or deletion as requested by ImGui."""
        if tex.status == imgui.ImTextureStatus.want_create:
            _log_texture(f"UpdateTexture #{tex.unique_id}: WantCreate {tex.width}x{tex.height}")
            assert tex.tex_id == 0 and tex.backend_user_data is None
            assert tex.format == imgui.ImTextureFormat.rgba32
            new_tex_id = self._tex_create(tex)
            tex.set_tex_id(new_tex_id)
            tex.status = imgui.ImTextureStatus.ok

        elif tex.status == imgui.ImTextureStatus.want_updates:
            _log_texture(f"UpdateTexture #{tex.unique_id}: WantUpdate {len(tex.updates)}")
            full_pixels = tex.get_pixels_array()
            for r in tex.updates:
                self._tex_update_subrect(tex, r, full_pixels)
            tex.status = imgui.ImTextureStatus.ok

        elif tex.status == imgui.ImTextureStatus.want_destroy:
            _log_texture(f"UpdateTexture #{tex.unique_id}: WantDestroy")
            self._tex_delete(tex.tex_id)
            tex.set_tex_id(0)
            tex.status = imgui.ImTextureStatus.destroyed

    def _tex_create(self, tex: imgui.ImTextureData) -> int:
        """Allocate a new OpenGL texture for an ImGui ImTextureData object."""
        pixels = tex.get_pixels_array()
        obj = self.ctx.texture((tex.width, tex.height), 4, pixels)
        obj.filter = (moderngl.LINEAR, moderngl.LINEAR)
        obj.repeat_x = False
        obj.repeat_y = False
        self._textures[obj.glo] = obj
        return obj.glo

    def _tex_update_subrect(self, tex: imgui.ImTextureData, r, full_pixels) -> None:
        """Update a sub-rectangle of an existing texture."""
        obj = self._textures.get(tex.tex_id)
        if not obj:
            _log_texture(f"Missing texture #{tex.unique_id} during update")
            return
        sub = full_pixels.reshape(tex.height, tex.width,
                                  tex.bytes_per_pixel)[r.y:r.y + r.h, r.x:r.x + r.w]
        obj.write(sub.tobytes(), viewport=(r.x, r.y, r.w, r.h))

    def _tex_delete(self, tex_id: int) -> None:
        """Delete an OpenGL texture associated with ImGui."""
        obj = self._textures.pop(tex_id, None)
        if obj:
            obj.release()

    # -------------------------------------------------------------------------
    # --- Rendering ------------------------------------------------------------
    # -------------------------------------------------------------------------

    def render(self, draw_data: imgui.ImDrawData) -> None:
        """Render the ImGui draw lists using ModernGL."""
        io = self.io
        display_width, display_height = io.display_size
        fb_width = int(display_width * io.display_framebuffer_scale[0])
        fb_height = int(display_height * io.display_framebuffer_scale[1])

        # Update ImGui’s texture state before drawing
        self._update_textures()

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
                tex_id = command.get_tex_id()
                texture = self._textures.get(tex_id)
                if texture is None:
                    raise ValueError(
                        f"Texture {tex_id} is not registered. "
                        f"Add via register_texture(..). Current: {list(self._textures)}"
                    )
                texture.use(0)

                x, y, z, w = command.clip_rect
                self.ctx.scissor = int(x), int(fb_height - w), int(z - x), int(w - y)
                self._vao.render(moderngl.TRIANGLES, vertices=command.elem_count, first=idx_pos)
                idx_pos += command.elem_count

        self.ctx.scissor = None

    # -------------------------------------------------------------------------
    # --- Device Objects -------------------------------------------------------
    # -------------------------------------------------------------------------

    def _create_device_objects(self):
        """Create shaders, buffers, and VAO."""
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

    def _invalidate_device_objects(self):
        """Free all GL resources."""
        for obj in (self._vertex_buffer, self._index_buffer, self._vao, self._prog):
            if obj:
                obj.release()

    # -------------------------------------------------------------------------
    # --- Public API -----------------------------------------------------------
    # -------------------------------------------------------------------------

    def register_texture(self, texture: moderngl.Texture) -> None:
        """Make ImGui aware of an existing ModernGL texture."""
        self._textures[texture.glo] = texture

    def remove_texture(self, texture: moderngl.Texture) -> None:
        """Unregister a ModernGL texture from ImGui."""
        self._textures.pop(texture.glo, None)

    def shutdown(self) -> None:
        """Release all GL and ImGui resources."""
        self._destroy_all_textures()
        imgui.get_platform_io().textures.clear()
        imgui.get_io().backend_flags &= ~imgui.BackendFlags_.renderer_has_textures.value
        self._invalidate_device_objects()


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
