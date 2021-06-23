
Basic usage (WindowConfig)
==========================

.. note:: This section is only relevant when using
   :py:class:`~moderngl_window.context.base.window.WindowConfig`.
   Go to the Custom Usage section if you provide your own window
   and context or want more control.

Using the :py:class:`~moderngl_window.context.base.window.WindowConfig`
interface is the simplest way to start with moderngl-window.
This can work for smaller projects and implies that this library
provides the window and moderngl context.

The API docs for this class alone should cover a lot of ground,
but we'll go through the basics here.

Basic example
-------------

The :py:class:`~moderngl_window.context.base.window.WindowConfig` is
simply a class you extend to customize/implement initialization,
window parameters, rendering code, keyboard input, mouse input
and access simpler shortcut methods for loading resources.

.. code:: python

    import moderngl_window as mglw

    class Test(mglw.WindowConfig):
        gl_version = (3, 3)
        window_size = (1920, 1080)

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Do initialization here
            self.prog = self.ctx.program(...)
            self.vao = self.ctx.vertex_array(...)
            self.texture = self.ctx.texture(self.wnd.size, 4)

        def render(self, time, frametime):
            # This method is called every frame
            self.vao.render()

    # Blocking call entering rendering/event loop
    mglw.run_window_config(Test)

The :py:class:`~moderngl_window.context.base.window.WindowConfig`
instance will by default receive three external instances in ``__init__``
that can be accessed later with ``self``.

- ``self.ctx``: The ``moderngl.Context`` created by the configured window type
- ``self.wnd``: The window instance
- ``self.timer``: The :py:class:`moderngl_window.timers.clock.Timer`
  instance to control the current time (Values passed into ``render``)

Resource loading
----------------

The :py:class:`~moderngl_window.context.base.window.WindowConfig` class has
built in shortcuts to the resource loading system.

.. code:: python

    self.load_texture_2d('background.png')
    self.load_texture_array('tiles.png', layers=16)
    self.load_program('myprogram.glsl')
    self.load_text('textfile.txt')
    self.load_json('config.json')
    self.load_binary('data.bin')
    self.load_scene('cube.obj')
    self.load_scene('city.gltf')

All paths used in resource loading are relative to an absolute path
provided in the :py:class:`~moderngl_window.context.base.window.WindowConfig`.

.. code:: python

    from pathlib import Path

    class Test(mglw.WindowConfig):
        resource_dir = (Path(__file__).parent / 'resources').resolve()

If you need more than one search path for your resources, the
:py:mod:`moderngl_window.resources` module has methods for this.

Optionally an absolute path can be used to load a file at a
specific location bypassing the entire resource system.
This is not recommended, but is useful in some situations.

Generic events and window types
-------------------------------

The :py:class:`~moderngl_window.context.base.window.WindowConfig`
interface depends on the built in window types or a self-provided
window implementation of
:py:class:`~moderngl_window.context.base.window.BaseWindow`.
These window implementations convert window, key and mouse events
into a unified system so the user can switch between different window
types without altering the code.

Window libraries are not perfect and may at times work sub-optimally
on some platforms. They might also have different performance profiles.
The ability to switch between window types by just changing a config
value can be an advantage.

You can change what window class is used by passing in the
``--window`` option. Optionally you can modify the
:py:attr:`~moderngl_window.conf.Settings.WINDOW` attribute directly.

Command line arguments
----------------------

The :py:func:`~moderngl_window.run_window_config` method also reads arguments
from ``sys.argv`` making the user able to override config values in the class.

Example::

    python test.py --window glfw --fullscreen --vsync --samples 16 --cursor false --size 800x600

See code for :py:func:`moderngl_window.parse_args` for more details.

Window events
-------------

.. code:: python

    def resize(self, width: int, height: int):
        print("Window was resized. buffer size is {} x {}".format(width, height))

    def close(self):
        print("The window is closing")

    def iconify(self, iconify: bool):
        print("Window was iconified:", iconify)

Keyboard input
--------------

Implement the ``key_event`` and ``unicode_char_entered`` method to handle
key events.

.. code:: python

    def key_event(self, key, action, modifiers):
        # Key presses
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.SPACE:
                print("SPACE key was pressed")

            # Using modifiers (shift and ctrl)

            if key == self.wnd.keys.Z and modifiers.shift:
                print("Shift + Z was pressed")

            if key == self.wnd.keys.Z and modifiers.ctrl:
                print("ctrl + Z was pressed")

        # Key releases
        elif action == self.wnd.keys.ACTION_RELEASE:
            if key == self.wnd.keys.SPACE:
                print("SPACE key was released")

    def unicode_char_entered(self, char: str):
        print('character entered:', char)


Mouse input
-----------

Implement the ``mouse_*`` methods to handle mouse input.

.. code:: python

    def mouse_position_event(self, x, y, dx, dy):
        print("Mouse position:", x, y, dx, dy)

    def mouse_drag_event(self, x, y, dx, dy):
        print("Mouse drag:", x, y, dx, dy)

    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        print("Mouse wheel:", x_offset, y_offset)

    def mouse_press_event(self, x, y, button):
        print("Mouse button {} pressed at {}, {}".format(button, x, y))

    def mouse_release_event(self, x: int, y: int, button: int):
        print("Mouse button {} released at {}, {}".format(button, x, y))
