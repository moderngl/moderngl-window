# moderngl_window

**WORK IN PROGRESS**: This package is currently under development. It will
be released with PyPI packages soon. Testing and feedback is appreciated.

Easily create a window for ModernGL using the most popular window libraries

* moderngl_window documentation
* moderngl_window on PyPI
* [moderngl_window on Github](https://github.com/moderngl/moderngl_window)
* [ModernGL](https://github.com/moderngl/moderngl)

## Features

* Easily create a window for ModernGL using Pyglet, PyQt5, GLFW or SDL2 supporing basic keyboard and mouse controls in a generic way.

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
