# moderngl_window

**WORK IN PROGRESS**: This is currently only a direct copy of `moderngl/examples/window`
and is not a working package at this moment.

Easily create a window for ModernGL using the most popular window libraries

* [moderngl_window documenation]()
* [moderngl_window on PyPI]()
* [moderngl_window on Github]()
* [ModernGL](https://github.com/cprogrammer1994/ModernGL)

## Features

* Easily create a window for ModernGL using PyQt5, GLFW, SDL2 or Pyglet supporing basic keyboard and mouse controls in a generic way.

## Supported Platforms

- [x] Windows
- [x] Linux
- [x] Mac OS X

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


mglw.run_example(Test)
```
