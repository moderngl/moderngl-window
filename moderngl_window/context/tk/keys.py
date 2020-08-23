# flake8: noqa E741
from moderngl_window.context.base import BaseKeys


class Keys(BaseKeys):
    """
    Namespace mapping tkinter keys.
    Maps the keysym strings provided in tk.Events
    """

    # TODO: We might want to use keycode instead if this works cross platform.
    #       Right now upper case characters will not be recognized.
    #
    # Possibly we need to separate actual characters and control keys.
    #
    # <KeyPress event state=Mod1 keysym=d keycode=68 char='d'>
    # <KeyPress event state=Shift|Mod1 keysym=D keycode=68 char='D'>
    #
    # See : https://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
    ESCAPE = "Escape"
    SPACE = " "
    ENTER = "Return"
    PAGE_UP = "Prior"
    PAGE_DOWN = "Next"
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"

    TAB = "Tab"
    COMMA = "comma"
    MINUS = "minus"
    PERIOD = "period"
    SLASH = "slash"
    SEMICOLON = "semicolon"
    EQUAL = "equal"
    LEFT_BRACKET = "bracketleft"
    RIGHT_BRACKET = "bracketright"
    BACKSLASH = "backslash"
    BACKSPACE = "BackSpace"
    INSERT = "Insert"
    DELETE = "Delete"
    HOME = "Home"
    END = "End"
    CAPS_LOCK = "Caps_Lock"

    F1 = "F1"
    F2 = "F2"
    F3 = "F3"
    F4 = "F4"
    F5 = "F5"
    F6 = "F6"
    F7 = "F7"
    F8 = "F8"
    F9 = "F9"
    F10 = "F10"
    F11 = "F11"
    F12 = "F12"

    NUMBER_0 = "0"
    NUMBER_1 = "1"
    NUMBER_2 = "2"
    NUMBER_3 = "3"
    NUMBER_4 = "4"
    NUMBER_5 = "5"
    NUMBER_6 = "6"
    NUMBER_7 = "7"
    NUMBER_8 = "8"
    NUMBER_9 = "9"

    NUMPAD_0 = "0"
    NUMPAD_1 = "1"
    NUMPAD_2 = "2"
    NUMPAD_3 = "3"
    NUMPAD_4 = "4"
    NUMPAD_5 = "5"
    NUMPAD_6 = "6"
    NUMPAD_7 = "7"
    NUMPAD_8 = "8"
    NUMPAD_9 = "9"

    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"
    H = "h"
    I = "i"
    J = "j"
    K = "k"
    L = "l"
    M = "m"
    N = "n"
    O = "o"
    P = "p"
    Q = "q"
    R = "r"
    S = "s"
    T = "t"
    U = "u"
    V = "v"
    W = "w"
    X = "x"
    Y = "y"
    Z = "z"
