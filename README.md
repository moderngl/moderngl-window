[![pypi](https://badge.fury.io/py/moderngl-window.svg)](https://pypi.python.org/pypi/moderngl-window) [![rtd](https://readthedocs.org/projects/moderngl-window/badge/?version=latest)](https://moderngl-window.readthedocs.io)

# moderngl-window

A cross platform utility library for [ModernGL](https://github.com/moderngl/moderngl) making window
creation and resource loading simple. It can also be used with PyOpenGL for
rendering with the programmable pipeline.

* [moderngl-window Documentation](https://moderngl-window.readthedocs.io)
* [moderngl-window on PyPI](https://pypi.org/project/moderngl-window)
* [moderngl-window on Github](https://github.com/moderngl/moderngl-window)
* [ModernGL](https://github.com/moderngl/moderngl)
* [ModernGL Discord Server](https://discord.gg/UEMtW8D)

Please report bugs or post questions/feedback on [github](https://github.com/moderngl/moderngl-window/issues).

## Features

* Cross platform support. Tested on Windows 10, Linux and Mac OS X.
  This can save users a lot of time and is often more difficult than most people
  imagine it to be.
* Easily create a window for ModernGL using pyglet, pygame, PySide2, GLFW, SDL2, PyQt5
  or tkinter supporting a wide range of window, keyboard and mouse events.
  These events are unified into a single system so your project can work with any window.
* Load 2D textures, texture arrays and cube maps using Pillow
* Load shaders as single or multiple `glsl` files
* Load objects/scenes from wavefront/obj, GLTF 2.0 or STL
* Resource finder system supporting multiple resource directories
* A highly plugable library supporting custom loaders,
  resource finders and windows.
* Type hints everywhere making code completion and linting a breeze

We are not trying to force the user into using every aspect of this
library. If you have an exiting project and just need texture loading
you will be able to do this without unnecessary hurdles as long as
you provide us your `moderngl.Context`.

## Install

```bash
pip install moderngl-window
```

## Supported Platforms

* [x] Windows
* [x] Linux
* [x] Mac OS X

## Sample Usage

Simple example opening a window clearing every frame using red (color).

```py
# test.py
import moderngl_window as mglw

class Test(mglw.WindowConfig):
    gl_version = (3, 3)

    def render(self, time, frametime):
        self.ctx.clear(1.0, 0.0, 0.0, 0.0)

Test.run()
```

Run the example with different window backends:

```bash
python test.py --window pyglet
python test.py --window pygame2
python test.py --window glfw
python test.py --window sdl2
python test.py --window pyside2
python test.py --window pyqt5
python test.py --window tk
```

`WindowConfig` classes are the simplest way to get started without knowing
a lot about this library. For more advanced usage see documentation
or examples.

## Setup from source

We assume the user knows how to handle virtualenvs.

```bash
# Install the package in editable mode
$ pip install -e .

# Install development requirements
$ pip install -e .[dev]
```

## Running Tests

With dev requirements installed:

```
pytest
```

## Building Docs

```bash
pip install -e .[dev]
sphinx-build -b html docs docs/_build
```

## Contributing

Contributions are welcome regardless of experience level.
Don't hesitate submitting issues, opening partial or completed
pull requests.

### Plugins

We are interested in contributions providing new loaders, windows etc.
For these to be included in this library we require them
to work cross platforms (win10/linux/osx) and be fairly easy to set up.

If it requires more than manually downloading a pre-compiled dll
(like SDL2, GLFW etc.) it would most likely not be included,
but you are welcome to present your case if you still think it should
be included.

If you create your own repo/package containing plugins for
this library, please make an issue and we'll link back to it.
Be sure to include what platforms are supported, install
instructions, how you configure it in `moderngl-window` and
of course a clear and concise description of what exactly
your package provides.

## Citation

If you need to cite this repository in academic research:

```txt
@Online{Forselv2020,
  author = {Einar Forselv},
  title = {moderngl-window, a cross-platform windowing/utility library for ModernGL},
  date = {2020-05-01},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/moderngl/moderngl-window}},
  commit = {<insert hash if needed>}
}
```

If commit hash is required this can be found per release here:
<https://github.com/moderngl/moderngl-window/releases>

## Attributions

We can't build everything from scratch. We rely on certain packages
and resources to make this project possible.

### Windows

* pyglet (<https://github.com/pyglet/pyglet>)
* pygame (<https://github.com/pygame/pygame>)
* pyGLFW (<https://github.com/FlorianRhiem/pyGLFW>)
* PySDL2 (<https://github.com/marcusva/py-sdl2>)
* PySide2 (<https://wiki.qt.io/Qt_for_Python>)
* PyQt5 (<https://www.riverbankcomputing.com/software/pyqt/intro>)
* tkinter (<https://github.com/jonwright/pyopengltk>)

### Loaders

* Pillow (<https://python-pillow.org/>)
* pywavefront (<https://github.com/pywavefront/PyWavefront>)
* trimesh (<https://github.com/mikedh/trimesh>)

### Testing & Utility

* PyGLM (<https://github.com/Zuzu-Typ/PyGLM>)
* ruff (<https://github.com/astral-sh/ruff>)
* numpy (<https://github.com/numpy/numpy>)
* pytest (<https://docs.pytest.org/en/latest/>)
* coverage (<https://github.com/nedbat/coveragepy>)

## Resources

* NASA 3D Resources (<https://github.com/nasa/NASA-3D-Resources>)
* glTF Sample Models (<https://github.com/KhronosGroup/glTF-Sample-Models>)

## Some History

The majority of the code in this library comes from [demosys-py](https://github.com/Contraz/demosys-py) (somewhat modified).
Because `demosys-py` is a framework we decided to split out a lot useful functionality into this
library. Frameworks are a lot less appealing to users and it would be a shame to not make this
more available to the ModernGL user base.
