import moderngl_window as mglw


class BasicWindowConfig(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Basic Window Config"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, time, frametime):
        pass


if __name__ == '__main__':
    mglw.run_window_config(BasicWindowConfig)
