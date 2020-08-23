# flake8: noqa E741
import pygame

from moderngl_window.context.base import BaseKeys


class Keys(BaseKeys):
    """
    Namespace mapping pygame2 specific key constants
    """

    ACTION_PRESS = pygame.KEYDOWN
    ACTION_RELEASE = pygame.KEYUP

    ESCAPE = pygame.K_ESCAPE
    SPACE = pygame.K_SPACE
    ENTER = pygame.K_RETURN
    PAGE_UP = pygame.K_PAGEUP
    PAGE_DOWN = pygame.K_PAGEDOWN
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN

    TAB = pygame.K_TAB
    COMMA = pygame.K_COMMA
    MINUS = pygame.K_MINUS
    PERIOD = pygame.K_PERIOD
    SLASH = pygame.K_SLASH
    SEMICOLON = pygame.K_SEMICOLON
    EQUAL = pygame.K_EQUALS
    LEFT_BRACKET = pygame.K_LEFTBRACKET
    RIGHT_BRACKET = pygame.K_RIGHTBRACKET
    BACKSLASH = pygame.K_BACKSLASH
    BACKSPACE = pygame.K_BACKSPACE
    INSERT = pygame.K_INSERT
    DELETE = pygame.K_DELETE
    HOME = pygame.K_HOME
    END = pygame.K_END
    CAPS_LOCK = pygame.K_CAPSLOCK

    F1 = pygame.K_F1
    F2 = pygame.K_F2
    F3 = pygame.K_F3
    F4 = pygame.K_F4
    F5 = pygame.K_F5
    F6 = pygame.K_F6
    F7 = pygame.K_F7
    F8 = pygame.K_F8
    F9 = pygame.K_F9
    F10 = pygame.K_F10
    F11 = pygame.K_F11
    F12 = pygame.K_F12

    NUMBER_0 = pygame.K_0
    NUMBER_1 = pygame.K_1
    NUMBER_2 = pygame.K_2
    NUMBER_3 = pygame.K_3
    NUMBER_4 = pygame.K_4
    NUMBER_5 = pygame.K_5
    NUMBER_6 = pygame.K_6
    NUMBER_7 = pygame.K_7
    NUMBER_8 = pygame.K_8
    NUMBER_9 = pygame.K_9

    NUMPAD_0 = pygame.K_KP_0
    NUMPAD_1 = pygame.K_KP_1
    NUMPAD_2 = pygame.K_KP_2
    NUMPAD_3 = pygame.K_KP_3
    NUMPAD_4 = pygame.K_KP_4
    NUMPAD_5 = pygame.K_KP_5
    NUMPAD_6 = pygame.K_KP_6
    NUMPAD_7 = pygame.K_KP_7
    NUMPAD_8 = pygame.K_KP_8
    NUMPAD_9 = pygame.K_KP_9

    A = pygame.K_a
    B = pygame.K_b
    C = pygame.K_c
    D = pygame.K_d
    E = pygame.K_e
    F = pygame.K_f
    G = pygame.K_g
    H = pygame.K_h
    I = pygame.K_i
    J = pygame.K_j
    K = pygame.K_k
    L = pygame.K_l
    M = pygame.K_m
    N = pygame.K_n
    O = pygame.K_o
    P = pygame.K_p
    Q = pygame.K_q
    R = pygame.K_r
    S = pygame.K_s
    T = pygame.K_t
    U = pygame.K_u
    V = pygame.K_v
    W = pygame.K_w
    X = pygame.K_x
    Y = pygame.K_y
    Z = pygame.K_z
