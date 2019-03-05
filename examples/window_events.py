import moderngl_window as mglw


class WindowEvents(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Window Events"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, time, frametime):
        if self.wnd.is_key_pressed(self.wnd.keys.SPACE):
            print("User is holding SPACE button")

    def key_event(self, key, action):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.SPACE:
                print("SPACE key was pressed")

        elif action == self.wnd.keys.ACTION_RELEASE:
            if key == self.wnd.keys.SPACE:
                print("SPACE key was released")

    def mouse_position_event(self, x, y):
        print("Mouse position:", x, y)

    def mouse_press_event(self, x, y, button):
        print("Mouse button {} pressed at {}, {}".format(button, x, y))

    def mouse_release_event(self, x: int, y: int, button: int):
        print("Mouse button {} released at {}, {}".format(button, x, y))


mglw.run_window_config(WindowEvents)
