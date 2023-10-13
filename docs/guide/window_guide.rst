
Window Guide
============

We support the following window types:

* pyglet
* glfw
* sdl2
* pygame2
* pyside2
* pyqt5
* tk
* headless

Using built in window types
---------------------------

The library provides shortcuts for window creation
in the :py:mod:`moderngl_window` module that will
also handle context activation.

The :py:class:`moderngl_window.conf.Settings` instance
has sane default parameters for a window.
See the :py:attr:`~moderngl_window.conf.Settings.WINDOW` attribute.

.. code:: python

    import moderngl_window
    from moderngl_window.conf import settings

    settings.WINDOW['class'] = 'moderngl_window.context.glfw.Window'
    settings.WINDOW['gl_version'] = (4, 1)
    # ... etc ...

    # Creates the window instance and activates its context
    window = moderngl_window.create_window_from_settings()

There are more sane ways to apply different configuration values
through convenient methods in the :py:class:`~moderngl_window.conf.Settings`
class.

Window classes can of course also be instantiated manually if
preferred, but this can generate a bit of extra work.

.. code:: python

    import moderngl_window

    window_str = 'moderngl_window.context.pyglet.Window'
    window_cls = moderngl_window.get_window_cls(window_str)
    window = window_cls(
        title="My Window",
        gl_version=(4, 1),
        size=(1920, 1080),
        ...,
    )
    moderngl_window.activate_context(ctx=window.ctx)

You could also simply import the class directory and instantiate it,
but that defeats the purpose of trying to be independent of a specific
window library.

The rendering loop for built in windows is simple:

.. code:: python

    while not window.is_closing:
        window.clear()
        # Render stuff here
        window.swap_buffers()

The ``swap_buffers`` method is important as it also pulls new input
events for the next frame.


Old Guide
=========

When not using a :py:class:`~moderngl_window.context.base.window.WindowConfig`
instance, there are a few simple steps to get started.

Register the moderngl.Context
-----------------------------

When not using the built in window types you need to at least tell
moderngl_window what your ``moderngl.Context`` is.

.. code:: python

    import moderngl
    import moderngl_window

    # Somewhere in your application a standalone or normal context is created
    ctx = moderngl.create_standalone_context(require=330)
    ctx = moderngl.create_context(require=330)

    # Make sure you activate this context
    moderngl_window.activate_context(ctx=ctx)

If there is no context activated the library will raise an exception
when doing operations that requires one, such as texture and scene
loading.

When using the built in window types the context activation
is normally done for you on creation.

Register resource directories
-----------------------------

The resource loading system uses relative paths. These paths
are relative to one or multiple directories we registered in the
resource system.

The :py:mod:`moderngl_window.resources` module has methods for this.

.. code:: python

    from pathlib import Path
    from moderngl_window import resources

    # We recommend using pathlib
    resources.register_dir(Path('absolute/path/to/resource/dir').resolve())
    # .. but strings also works
    resources.register_dir('absolute/path/to/resource/dir')

These need to be absolute paths or an exception is raised.
You can register as many paths as you want. The resource
system will simply look for the file in every registered
directory in the order they were added until it finds a match.

This library also supports separate search directories for
shader programs, textures, scenes and various data files.

