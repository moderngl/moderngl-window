# moderngl_window

**WORK IN PROGRESS**: This package is currently under development. It will
be released with PyPI packages soon. Testing and feedback is appreciated.

Easily create a window for ModernGL using the most popular window libraries

* moderngl_window documentation
* moderngl_window on PyPI
* [moderngl_window on Github](https://github.com/moderngl/moderngl_window)
* [ModernGL](https://github.com/moderngl/moderngl)

## Features

* Easily create a window for ModernGL using Pyglet, PyQt5, GLFW or SDL2 supporing basic keyboard and mouse controls in a generic way
* Easily load resources like textures, shaders, objects/scenes
* A highly pluggable library. Create your own window types and loaders

Also keep in mind this is a library. You are not required to use
the windows or resource loaders we provide. It's all up to you.
Just provide your `moderngl.Context` and you are good to go.

## Supported Platforms

* [x] Windows
* [x] Linux
* [x] Mac OS X

## Sample Usage

Simple example opening a window clearing it with a red color every frame.

```py
import moderngl_window as mglw


class Test(mglw.WindowConfig):
    gl_version = (3, 3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, time, frametime):
        self.ctx.clear(1.0, 0.0, 0.0, 0.0)


mglw.run_window_config(Test)
```

## Some history about this library

The majority of the code in this library comes from [demosys-py](https://github.com/Contraz/demosys-py) (somewhat modified).
Because `demosys-py` is a framework we decided to split out a lot useful funtionality into this
library. Frameworks are a lot less appealing to users and it would be a shame to not make this
more avaialble to the ModernGL user base.
