# flake8: noqa E741

class KeyModifiers:
    """Namespace for storing key modifiers"""
    shift = False
    ctrl = False
    alt = False

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "<KeyModifiers shift={} ctrl={} alt={}".format(self.shift, self.ctrl, self.alt)


class BaseKeys:
    """
    Namespace for mapping key constants.
    This is simply a template for what keys should be mapped for all window libraries
    """
    # Fallback press/release action when window libraries don't have this
    ACTION_PRESS = 'ACTION_PRESS'
    ACTION_RELEASE = 'ACTION_RELEASE'

    ESCAPE = None
    SPACE = None
    ENTER = None
    PAGE_UP = None
    PAGE_DOWN = None
    LEFT = None
    RIGHT = None
    UP = None
    DOWN = None

    TAB = None
    COMMA = None
    MINUS = None
    PERIOD = None
    SLASH = None
    SEMICOLON = None
    EQUAL = None
    LEFT_BRACKET = None
    RIGHT_BRACKET = None
    BACKSLASH = None
    BACKSPACE = None
    INSERT = None
    DELETE = None
    HOME = None
    END = None
    CAPS_LOCK = None

    F1 = None
    F2 = None
    F3 = None
    F4 = None
    F5 = None
    F6 = None
    F7 = None
    F8 = None
    F9 = None
    F10 = None
    F11 = None
    F12 = None

    NUMBER_0 = None
    NUMBER_1 = None
    NUMBER_2 = None
    NUMBER_3 = None
    NUMBER_4 = None
    NUMBER_5 = None
    NUMBER_6 = None
    NUMBER_7 = None
    NUMBER_8 = None
    NUMBER_9 = None

    A = None
    B = None
    C = None
    D = None
    E = None
    F = None
    G = None
    H = None
    I = None
    J = None
    K = None
    L = None
    M = None
    N = None
    O = None
    P = None
    Q = None
    R = None
    S = None
    T = None
    U = None
    V = None
    W = None
    X = None
    Y = None
    Z = None
