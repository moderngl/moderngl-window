import moderngl
import moderngl_window as mglw
from moderngl_window import geometry


class SimpleCube(mglw.WindowConfig):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cube = geometry.cube(size=(2, 2, 2))
        

    def render(self, time, frametime):
        pass


if __name__ == '__main__':
    mglw.run_window_config(SimpleCube)
