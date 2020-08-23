import math
import moderngl_window
import random


class WindowEvents(moderngl_window.WindowConfig):
    """
    Demonstrates handling mouse, keyboard, render and resize events
    """
    gl_version = (3, 3)
    title = "Window Events"
    cursor = True
    vsync = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.wnd.exit_key = None

    def render(self, time: float, frametime: float):
        self.ctx.clear(
            (math.sin(time) + 1.0) / 2,
            (math.sin(time + 2) + 1.0) / 2,
            (math.sin(time + 3) + 1.0) / 2,
        )

        # We can also check if a key is in press state here
        if self.wnd.is_key_pressed(self.wnd.keys.SPACE):
            print("User is holding SPACE button")

    def resize(self, width: int, height: int):
        print("Window was resized. buffer size is {} x {}".format(width, height))

    def close(self):
        print("Window is closing")

    def iconify(self, iconify: bool):
        """Window hide/minimize and restore"""
        print("Window was iconified:", iconify)

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        # Key presses
        if action == keys.ACTION_PRESS:
            if key == keys.ESCAPE:
                print("ESCAPE key was pressed")

            if key == keys.SPACE:
                print("SPACE key was pressed")

            # Using modifiers (shift and ctrl)

            if key == keys.Z and modifiers.shift:
                print("Shift + Z was pressed")

            if key == keys.Z and modifiers.ctrl:
                print("ctrl + Z was pressed")

            if key == keys.Z and modifiers.alt:
                print("alt + Z was pressed")

        # Key releases
        elif action == self.wnd.keys.ACTION_RELEASE:
            if key == keys.SPACE:
                print("SPACE key was released")

        if action == keys.ACTION_PRESS:
            # Move the window around with AWSD
            if key == keys.A:
                self.wnd.position = self.wnd.position[0] - 20, self.wnd.position[1]
            if key == keys.D:
                self.wnd.position = self.wnd.position[0] + 20, self.wnd.position[1]
            if key == keys.W:
                self.wnd.position = self.wnd.position[0], self.wnd.position[1] - 20
            if key == keys.S:
                self.wnd.position = self.wnd.position[0], self.wnd.position[1] + 20

            # Resize window around with Shift + AWSD
            if self.wnd.modifiers.shift and key == keys.A:
                self.wnd.size = self.wnd.size[0] - 50, self.wnd.size[1]
            if self.wnd.modifiers.shift and key == keys.D:
                self.wnd.size = self.wnd.size[0] + 50, self.wnd.size[1]
            if self.wnd.modifiers.shift and key == keys.W:
                self.wnd.size = self.wnd.size[0], self.wnd.size[1] - 50
            if self.wnd.modifiers.shift and key == keys.S:
                self.wnd.size = self.wnd.size[0], self.wnd.size[1] + 50

            # toggle cursor
            if key == keys.C:
                self.wnd.cursor = not self.wnd.cursor

            # Shuffle window tittle
            if key == keys.T:
                title = list(self.wnd.title)
                random.shuffle(title)
                self.wnd.title = ''.join(title)

            # Toggle mouse exclusivity
            if key == keys.M:
                self.wnd.mouse_exclusivity = not self.wnd.mouse_exclusivity

            # Check number vs. numpad
            if key == keys.NUMBER_0:
                print('NUMBER 0')

            if key == keys.NUMPAD_0:
                print('NUMPAD 0')

    def mouse_position_event(self, x, y, dx, dy):
        print("Mouse position pos={} {} delta={} {}".format(x, y, dx, dy))

    def mouse_drag_event(self, x, y, dx, dy):
        print("Mouse drag pos={} {} delta={} {}".format(x, y, dx, dy))

    def mouse_scroll_event(self, x_offset, y_offset):
        print("mouse_scroll_event", x_offset, y_offset)

    def mouse_press_event(self, x, y, button):
        print("Mouse button {} pressed at {}, {}".format(button, x, y))
        print("Mouse states:", self.wnd.mouse_states)

    def mouse_release_event(self, x: int, y: int, button: int):
        print("Mouse button {} released at {}, {}".format(button, x, y))
        print("Mouse states:", self.wnd.mouse_states)

    def unicode_char_entered(self, char):
        print("unicode_char_entered:", char)


if __name__ == '__main__':
    moderngl_window.run_window_config(WindowEvents)
