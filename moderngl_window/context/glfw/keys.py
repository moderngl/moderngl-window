# flake8: noqa E741
import glfw

from moderngl_window.context.base import BaseKeys

GLFW_key = int


class Keys(BaseKeys):
    """
    Namespace defining glfw specific keys constants
    """

    ACTION_PRESS = glfw.PRESS
    ACTION_RELEASE = glfw.RELEASE

    ESCAPE = glfw.KEY_ESCAPE
    SPACE = glfw.KEY_SPACE
    ENTER = glfw.KEY_ENTER
    PAGE_UP = glfw.KEY_PAGE_UP
    PAGE_DOWN = glfw.KEY_PAGE_DOWN
    LEFT = glfw.KEY_LEFT
    RIGHT = glfw.KEY_RIGHT
    UP = glfw.KEY_UP
    DOWN = glfw.KEY_DOWN

    TAB = glfw.KEY_TAB
    COMMA = glfw.KEY_COMMA
    MINUS = glfw.KEY_MINUS
    PERIOD = glfw.KEY_PERIOD
    SLASH = glfw.KEY_SLASH
    SEMICOLON = glfw.KEY_SEMICOLON
    EQUAL = glfw.KEY_EQUAL
    LEFT_BRACKET = glfw.KEY_LEFT_BRACKET
    RIGHT_BRACKET = glfw.KEY_RIGHT_BRACKET
    BACKSLASH = glfw.KEY_BACKSLASH
    BACKSPACE = glfw.KEY_BACKSPACE
    INSERT = glfw.KEY_INSERT
    DELETE = glfw.KEY_DELETE
    HOME = glfw.KEY_HOME
    END = glfw.KEY_END
    CAPS_LOCK = glfw.KEY_CAPS_LOCK

    F1 = glfw.KEY_F1
    F2 = glfw.KEY_F2
    F3 = glfw.KEY_F3
    F4 = glfw.KEY_F4
    F5 = glfw.KEY_F5
    F6 = glfw.KEY_F6
    F7 = glfw.KEY_F7
    F8 = glfw.KEY_F8
    F9 = glfw.KEY_F9
    F10 = glfw.KEY_F10
    F11 = glfw.KEY_F11
    F12 = glfw.KEY_F12

    NUMBER_0 = glfw.KEY_0
    NUMBER_1 = glfw.KEY_1
    NUMBER_2 = glfw.KEY_2
    NUMBER_3 = glfw.KEY_3
    NUMBER_4 = glfw.KEY_4
    NUMBER_5 = glfw.KEY_5
    NUMBER_6 = glfw.KEY_6
    NUMBER_7 = glfw.KEY_7
    NUMBER_8 = glfw.KEY_8
    NUMBER_9 = glfw.KEY_9

    NUMPAD_0 = glfw.KEY_KP_0
    NUMPAD_1 = glfw.KEY_KP_1
    NUMPAD_2 = glfw.KEY_KP_2
    NUMPAD_3 = glfw.KEY_KP_3
    NUMPAD_4 = glfw.KEY_KP_4
    NUMPAD_5 = glfw.KEY_KP_5
    NUMPAD_6 = glfw.KEY_KP_6
    NUMPAD_7 = glfw.KEY_KP_7
    NUMPAD_8 = glfw.KEY_KP_8
    NUMPAD_9 = glfw.KEY_KP_9

    A = glfw.KEY_A
    B = glfw.KEY_B
    C = glfw.KEY_C
    D = glfw.KEY_D
    E = glfw.KEY_E
    F = glfw.KEY_F
    G = glfw.KEY_G
    H = glfw.KEY_H
    I = glfw.KEY_I
    J = glfw.KEY_J
    K = glfw.KEY_K
    L = glfw.KEY_L
    M = glfw.KEY_M
    N = glfw.KEY_N
    O = glfw.KEY_O
    P = glfw.KEY_P
    Q = glfw.KEY_Q
    R = glfw.KEY_R
    S = glfw.KEY_S
    T = glfw.KEY_T
    U = glfw.KEY_U
    V = glfw.KEY_V
    W = glfw.KEY_W
    X = glfw.KEY_X
    Y = glfw.KEY_Y
    Z = glfw.KEY_Z
