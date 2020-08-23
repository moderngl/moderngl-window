# flake8: noqa E741
import sdl2

from moderngl_window.context.base import BaseKeys


class Keys(BaseKeys):
    """
    Namespace mapping SDL2 specific key constants
    """

    ACTION_PRESS = sdl2.SDL_KEYDOWN
    ACTION_RELEASE = sdl2.SDL_KEYUP

    ESCAPE = sdl2.SDLK_ESCAPE
    SPACE = sdl2.SDLK_SPACE
    ENTER = sdl2.SDLK_RETURN
    PAGE_UP = sdl2.SDLK_PAGEUP
    PAGE_DOWN = sdl2.SDLK_PAGEDOWN
    LEFT = sdl2.SDLK_LEFT
    RIGHT = sdl2.SDLK_RIGHT
    UP = sdl2.SDLK_UP
    DOWN = sdl2.SDLK_DOWN

    TAB = sdl2.SDLK_TAB
    COMMA = sdl2.SDLK_COMMA
    MINUS = sdl2.SDLK_MINUS
    PERIOD = sdl2.SDLK_PERIOD
    SLASH = sdl2.SDLK_SLASH
    SEMICOLON = sdl2.SDLK_SEMICOLON
    EQUAL = sdl2.SDLK_EQUALS
    LEFT_BRACKET = sdl2.SDLK_LEFTBRACKET
    RIGHT_BRACKET = sdl2.SDLK_RIGHTBRACKET
    BACKSLASH = sdl2.SDLK_BACKSLASH
    BACKSPACE = sdl2.SDLK_BACKSPACE
    INSERT = sdl2.SDLK_INSERT
    DELETE = sdl2.SDLK_DELETE
    HOME = sdl2.SDLK_HOME
    END = sdl2.SDLK_END
    CAPS_LOCK = sdl2.SDLK_CAPSLOCK

    F1 = sdl2.SDLK_F1
    F2 = sdl2.SDLK_F2
    F3 = sdl2.SDLK_F3
    F4 = sdl2.SDLK_F4
    F5 = sdl2.SDLK_F5
    F6 = sdl2.SDLK_F6
    F7 = sdl2.SDLK_F7
    F8 = sdl2.SDLK_F8
    F9 = sdl2.SDLK_F9
    F10 = sdl2.SDLK_F10
    F11 = sdl2.SDLK_F11
    F12 = sdl2.SDLK_F12

    NUMBER_0 = sdl2.SDLK_0
    NUMBER_1 = sdl2.SDLK_1
    NUMBER_2 = sdl2.SDLK_2
    NUMBER_3 = sdl2.SDLK_3
    NUMBER_4 = sdl2.SDLK_4
    NUMBER_5 = sdl2.SDLK_5
    NUMBER_6 = sdl2.SDLK_6
    NUMBER_7 = sdl2.SDLK_7
    NUMBER_8 = sdl2.SDLK_8
    NUMBER_9 = sdl2.SDLK_9

    NUMPAD_0 = sdl2.SDLK_KP_0
    NUMPAD_1 = sdl2.SDLK_KP_1
    NUMPAD_2 = sdl2.SDLK_KP_2
    NUMPAD_3 = sdl2.SDLK_KP_3
    NUMPAD_4 = sdl2.SDLK_KP_4
    NUMPAD_5 = sdl2.SDLK_KP_5
    NUMPAD_6 = sdl2.SDLK_KP_6
    NUMPAD_7 = sdl2.SDLK_KP_7
    NUMPAD_8 = sdl2.SDLK_KP_8
    NUMPAD_9 = sdl2.SDLK_KP_9

    A = sdl2.SDLK_a
    B = sdl2.SDLK_b
    C = sdl2.SDLK_c
    D = sdl2.SDLK_d
    E = sdl2.SDLK_e
    F = sdl2.SDLK_f
    G = sdl2.SDLK_g
    H = sdl2.SDLK_h
    I = sdl2.SDLK_i
    J = sdl2.SDLK_j
    K = sdl2.SDLK_k
    L = sdl2.SDLK_l
    M = sdl2.SDLK_m
    N = sdl2.SDLK_n
    O = sdl2.SDLK_o
    P = sdl2.SDLK_p
    Q = sdl2.SDLK_q
    R = sdl2.SDLK_r
    S = sdl2.SDLK_s
    T = sdl2.SDLK_t
    U = sdl2.SDLK_u
    V = sdl2.SDLK_v
    W = sdl2.SDLK_w
    X = sdl2.SDLK_x
    Y = sdl2.SDLK_y
    Z = sdl2.SDLK_z
