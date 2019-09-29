import moderngl_window as mglw


class WindowEvents(mglw.WindowConfig):
    """
    Demonstrates handling mouse, keyboard, render and resize events
    """
    gl_version = (3, 3)
    title = "Window Events"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, time: float, frametime: float):
        # We can also check if a key is in press state here
        if self.wnd.is_key_pressed(self.wnd.keys.SPACE):
            print("User is holding SPACE button")

    def resize(self, width: int, height: int):
        print("Window was resized. buffer size is {} x {}".format(width, height))

    def key_event(self, key, action, modifiers):
        # Key presses
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.SPACE:
                print("SPACE key was pressed")

            # Using modifiers (shift and ctrl)

            if key == self.wnd.keys.Z and modifiers.shift:
                print("Shift + Z was pressed")

            if key == self.wnd.keys.Z and modifiers.ctrl:
                print("ctrl + Z was pressed")

        # Key releases
        elif action == self.wnd.keys.ACTION_RELEASE:
            if key == self.wnd.keys.SPACE:
                print("SPACE key was released")

    def mouse_position_event(self, x, y):
        print("Mouse position:", x, y)

    def mouse_drag_event(self, x, y):
        print("Mouse drag:", x, y)

    def mouse_scroll_event(self, x_offset, y_offet):
        print("mouse_scroll_event", x_offset, y_offet)

    def mouse_press_event(self, x, y, button):
        print("Mouse button {} pressed at {}, {}".format(button, x, y))
        print("Mouse states:", self.wnd.mouse_states)

    def mouse_release_event(self, x: int, y: int, button: int):
        print("Mouse button {} released at {}, {}".format(button, x, y))
        print("Mouse states:", self.wnd.mouse_states)

    def unicode_char_entered(self, char):
        print("unicode_char_entered:", char)


if __name__ == '__main__':
    mglw.run_window_config(WindowEvents)
