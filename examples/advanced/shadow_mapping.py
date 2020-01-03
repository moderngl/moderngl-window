from pathlib import Path
import moderngl_window


class ShadowMapping(moderngl_window.WindowConfig):
    title = "Shadow Mapping"
    resource_dir = (Path(__file__) / '../../resources').resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.linearize_depth_program = self.load_program('programs/linearize_depth.glsl')

    def render(self, time, frametime):
        pass


if __name__ == '__main__':
    moderngl_window.run_window_config(ShadowMapping)
