from collections import namedtuple
from typing import Callable

from moderngl_window.context.base.keys import BaseKeys

KeyMap = namedtuple("KeyMap", ["UP", "DOWN", "LEFT", "RIGHT", "FORWARD", "BACKWARD"])

# A factory is used since we cannot deduce the keys format before run time, as they are
# induced by the window software used.
# Therefore, the factory takes as a parameter the keys used, and return a keymap instance.
KeyMapFactory = Callable[[BaseKeys], KeyMap]
AZERTY: KeyMapFactory = lambda keys: KeyMap(
    UP=keys.A, DOWN=keys.E, LEFT=keys.Q, RIGHT=keys.D, FORWARD=keys.Z, BACKWARD=keys.S
)
QWERTY: KeyMapFactory = lambda keys: KeyMap(
    UP=keys.Q, DOWN=keys.E, LEFT=keys.A, RIGHT=keys.D, FORWARD=keys.W, BACKWARD=keys.S
)
