# flake8: noqa E741
from typing import Any


class KeyModifiers:
    """Namespace for storing key modifiers"""

    shift: Any = False
    ctrl: Any = False
    alt: Any = False

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "<KeyModifiers shift={} ctrl={} alt={}>".format(self.shift, self.ctrl, self.alt)


class BaseKeys:
    """
    Namespace for mapping key constants.
    This is simply a template for what keys should be mapped for all window libraries
    """

    # Fallback press/release action when window libraries don't have this
    ACTION_PRESS: Any = "ACTION_PRESS"
    ACTION_RELEASE: Any = "ACTION_RELEASE"

    ESCAPE: Any = "undefined"
    SPACE: Any = "undefined"
    ENTER: Any = "undefined"
    PAGE_UP: Any = "undefined"
    PAGE_DOWN: Any = "undefined"
    LEFT: Any = "undefined"
    RIGHT: Any = "undefined"
    UP: Any = "undefined"
    DOWN: Any = "undefined"
    LEFT_SHIFT: Any = "undefined"
    RIGHT_SHIFT: Any = "undefined"
    LEFT_CTRL: Any = "undefined"

    TAB: Any = "undefined"
    COMMA: Any = "undefined"
    MINUS: Any = "undefined"
    PERIOD: Any = "undefined"
    SLASH: Any = "undefined"
    SEMICOLON: Any = "undefined"
    EQUAL: Any = "undefined"
    LEFT_BRACKET: Any = "undefined"
    RIGHT_BRACKET: Any = "undefined"
    BACKSLASH: Any = "undefined"
    BACKSPACE: Any = "undefined"
    INSERT: Any = "undefined"
    DELETE: Any = "undefined"
    HOME: Any = "undefined"
    END: Any = "undefined"
    CAPS_LOCK: Any = "undefined"

    F1: Any = "undefined"
    F2: Any = "undefined"
    F3: Any = "undefined"
    F4: Any = "undefined"
    F5: Any = "undefined"
    F6: Any = "undefined"
    F7: Any = "undefined"
    F8: Any = "undefined"
    F9: Any = "undefined"
    F10: Any = "undefined"
    F11: Any = "undefined"
    F12: Any = "undefined"

    NUMBER_0: Any = "undefined"
    NUMBER_1: Any = "undefined"
    NUMBER_2: Any = "undefined"
    NUMBER_3: Any = "undefined"
    NUMBER_4: Any = "undefined"
    NUMBER_5: Any = "undefined"
    NUMBER_6: Any = "undefined"
    NUMBER_7: Any = "undefined"
    NUMBER_8: Any = "undefined"
    NUMBER_9: Any = "undefined"

    NUMPAD_0: Any = "undefined"
    NUMPAD_1: Any = "undefined"
    NUMPAD_2: Any = "undefined"
    NUMPAD_3: Any = "undefined"
    NUMPAD_4: Any = "undefined"
    NUMPAD_5: Any = "undefined"
    NUMPAD_6: Any = "undefined"
    NUMPAD_7: Any = "undefined"
    NUMPAD_8: Any = "undefined"
    NUMPAD_9: Any = "undefined"

    A: Any = "undefined"
    B: Any = "undefined"
    C: Any = "undefined"
    D: Any = "undefined"
    E: Any = "undefined"
    F: Any = "undefined"
    G: Any = "undefined"
    H: Any = "undefined"
    I: Any = "undefined"
    J: Any = "undefined"
    K: Any = "undefined"
    L: Any = "undefined"
    M: Any = "undefined"
    N: Any = "undefined"
    O: Any = "undefined"
    P: Any = "undefined"
    Q: Any = "undefined"
    R: Any = "undefined"
    S: Any = "undefined"
    T: Any = "undefined"
    U: Any = "undefined"
    V: Any = "undefined"
    W: Any = "undefined"
    X: Any = "undefined"
    Y: Any = "undefined"
    Z: Any = "undefined"
