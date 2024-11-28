"""
Custom usage: window creation and mapping callbacks functions at module level
"""
import math
import random

import moderngl_window
from moderngl_window.conf import settings
from moderngl_window.timers.clock import Timer

window = None


def main():
    global window
    # Configure to use pyglet window
    settings.WINDOW['class'] = 'moderngl_window.context.pyglet.Window'
    window = moderngl_window.create_window_from_settings()

    # Map callback functions
    window.resize_func = resize
    window.iconify_func = iconify
    window.key_event_func = key_event
    window.mouse_position_event_func = mouse_position_event
    window.mouse_drag_event_func = mouse_drag_event
    window.mouse_scroll_event_func = mouse_scroll_event
    window.mouse_press_event_func = mouse_press_event
    window.mouse_release_event_func = mouse_release_event
    window.unicode_char_entered_func = unicode_char_entered

    timer = Timer()
    timer.start()

    while not window.is_closing:
        window.use()
        window.clear()

        time, frame_time = timer.next_frame()

        window.ctx.clear(
            (math.sin(time) + 1.0) / 2,
            (math.sin(time + 2) + 1.0) / 2,
            (math.sin(time + 3) + 1.0) / 2,
        )

        window.swap_buffers()

    window.destroy()


def render(time: float, frametime: float):
    # We can also check if a key is in press state here
    if window.is_key_pressed(window.keys.SPACE):
        print("User is holding SPACE button")


def resize(width: int, height: int):
    print("Window was resized. buffer size is {} x {}".format(width, height))


def iconify(iconify: bool):
    """Window hide/minimize and restore"""
    print("Window was iconified:", iconify)


def key_event(key, action, modifiers):
    keys = window.keys

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
    elif action == keys.ACTION_RELEASE:
        if key == keys.SPACE:
            print("SPACE key was released")

    # Move the window around with AWSD
    if action == keys.ACTION_PRESS:
        if key == keys.A:
            window.position = window.position[0] - 10, window.position[1]
        if key == keys.D:
            window.position = window.position[0] + 10, window.position[1]
        if key == keys.W:
            window.position = window.position[0], window.position[1] - 10
        if key == keys.S:
            window.position = window.position[0], window.position[1] + 10

        # toggle cursor
        if key == keys.C:
            window.cursor = not window.cursor

        # Shuffle window tittle
        if key == keys.T:
            title = list(window.title)
            random.shuffle(title)
            window.title = ''.join(title)

        # Toggle mouse exclusivity
        if key == keys.M:
            window.mouse_exclusivity = not window.mouse_exclusivity


def mouse_position_event(x, y, dx, dy):
    print("Mouse position pos={} {} delta={} {}".format(x, y, dx, dy))


def mouse_drag_event(x, y, dx, dy):
    print("Mouse drag pos={} {} delta={} {}".format(x, y, dx, dy))


def mouse_scroll_event(x_offset, y_offset):
    print("mouse_scroll_event", x_offset, y_offset)


def mouse_press_event(x, y, button):
    print("Mouse button {} pressed at {}, {}".format(button, x, y))
    print("Mouse states:", window.mouse_states)


def mouse_release_event(x: int, y: int, button: int):
    print("Mouse button {} released at {}, {}".format(button, x, y))
    print("Mouse states:", window.mouse_states)


def unicode_char_entered(char):
    print("unicode_char_entered:", char)


if __name__ == '__main__':
    main()
