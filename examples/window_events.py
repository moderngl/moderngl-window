import moderngl_window as mglw
import random


class WindowEvents(mglw.WindowConfig):
    """
    Demonstrates handling mouse, keyboard, render and resize events
    """
    gl_version = (3, 3)
    title = "Window Events"
    cursor = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, time: float, frametime: float):
        # We can also check if a key is in press state here
        if self.wnd.is_key_pressed(self.wnd.keys.SPACE):
            print("User is holding SPACE button")

    def resize(self, width: int, height: int):
        print("Window was resized. buffer size is {} x {}".format(width, height))

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        # Key presses
        if action == keys.ACTION_PRESS:
            if key == keys.SPACE:
                print("SPACE key was pressed")

            # Using modifiers (shift and ctrl)

            if key == keys.Z and modifiers.shift:
                print("Shift + Z was pressed")

            if key == keys.Z and modifiers.ctrl:
                print("ctrl + Z was pressed")

        # Key releases
        elif action == self.wnd.keys.ACTION_RELEASE:
            if key == keys.SPACE:
                print("SPACE key was released")

        # Move the window around with AWSD
        if action == keys.ACTION_PRESS:
            if key == keys.A:
                self.wnd.position = self.wnd.position[0] - 10, self.wnd.position[1]
            if key == keys.D:
                self.wnd.position = self.wnd.position[0] + 10, self.wnd.position[1]
            if key == keys.W:
                self.wnd.position = self.wnd.position[0], self.wnd.position[1] - 10
            if key == keys.S:
                self.wnd.position = self.wnd.position[0], self.wnd.position[1] + 10

            # toggle cursor
            if key == keys.C:
                self.wnd.cursor = not self.wnd.cursor

            # Shuffle window tittle
            if key == keys.T:
                title = list(self.wnd.title)
                random.shuffle(title)
                self.wnd.title = ''.join(title)

    def mouse_position_event(self, x, y, dx, dy):
        print("Mouse drag pos={} {} delta={} {}".format(x, y, dx, dy))

    def mouse_drag_event(self, x, y, dx, dy):
        print("Mouse drag pos={} {} delta={} {}".format(x, y, dx, dy))

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
