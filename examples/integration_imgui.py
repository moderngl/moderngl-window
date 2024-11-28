from pathlib import Path

import glm
import moderngl

# import imgui
from imgui_bundle import imgui

import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window.integrations.imgui_bundle import ModernglWindowRenderer


class WindowEvents(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "imgui Integration"
    resource_dir = (Path(__file__).parent / "resources").resolve()
    aspect_ratio = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        imgui.create_context()
        self.wnd.ctx.error
        self.imgui = ModernglWindowRenderer(self.wnd)

        self.cube = geometry.cube(size=(2, 2, 2))
        self.prog = self.load_program("programs/cube_simple.glsl")
        self.prog["color"].value = (1.0, 1.0, 1.0, 1.0)
        self.prog["m_camera"].write(glm.mat4())
        self.prog["m_proj"].write(glm.perspective(glm.radians(75), self.wnd.aspect_ratio, 1, 100))

    def on_render(self, time: float, frametime: float):
        rotation = glm.mat4(glm.quat(glm.vec3(time, time, time)))
        translation = glm.translate(glm.vec3(0.0, 0.0, -3.5))
        model = translation * rotation

        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.prog["m_model"].write(model)
        self.cube.render(self.prog)

        self.render_ui()

    def render_ui(self):
        imgui.new_frame()
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):
                clicked_quit, selected_quit = imgui.menu_item("Quit", "Cmd+Q", False, True)

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        imgui.show_demo_window()

        imgui.begin("Custom window", True)
        imgui.text("Bar")
        imgui.text_colored(imgui.ImVec4(0.2, 1.0, 0.0, 1.0), "Eggs")
        imgui.end()

        imgui.render()
        self.imgui.render(imgui.get_draw_data())

    def on_resize(self, width: int, height: int):
        self.prog["m_proj"].write(glm.perspective(glm.radians(75), self.wnd.aspect_ratio, 1, 100))
        self.imgui.resize(width, height)

    def on_key_event(self, key, action, modifiers):
        self.imgui.key_event(key, action, modifiers)

    def on_mouse_position_event(self, x, y, dx, dy):
        self.imgui.mouse_position_event(x, y, dx, dy)

    def on_mouse_drag_event(self, x, y, dx, dy):
        self.imgui.mouse_drag_event(x, y, dx, dy)

    def on_mouse_scroll_event(self, x_offset, y_offset):
        self.imgui.mouse_scroll_event(x_offset, y_offset)

    def on_mouse_press_event(self, x, y, button):
        self.imgui.mouse_press_event(x, y, button)

    def on_mouse_release_event(self, x: int, y: int, button: int):
        self.imgui.mouse_release_event(x, y, button)

    def on_unicode_char_entered(self, char):
        self.imgui.unicode_char_entered(char)


if __name__ == "__main__":
    mglw.run_window_config(WindowEvents)
