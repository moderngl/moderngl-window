# Changelog

## 3.0.3

* Fixed a potential division by zero issue in timers
* Fixed the video player example

Thanks to @Leterax for the contributions to this release.

## 3.0.2

* Fixed an issue causing `BaseWindow.init_mgl_context` to fail if no context
  creation callback was provided.

## 3.0.1

* Timers now have `fps` and `fps_average` properties for obtaining the current and average frame rate
* Added `WindowConfig.hidden_window_framerate_limit` limiting framerate when the window is hidden.
  The default value is currently 30 fps. This can be disabled by setting the value to 0.
  This change combats framerate spikes in the thousands when the window is minimized eating up
  battery life and resources.
* `WindowConfig.init_mgl_context` can now be implemented to completely override context creation.
* `run_window_config` was split into `create_window_config_instance` and `run_window_config_instance`
  making customization easier. `run_window_config` will still behave as before.
* Some doc improvements

## 3.0.0

* All callback functions now has an `on_` prefix meaning existing code will need updating. The old names was somewhat unambiguous and was a source of confusion. It also makes it easier to separate the callback functions from other methods.
  * `render` -> `on_render`
  * `resize` -> `on_resize`
  * `close` -> `on_close`
  * `iconify` -> `on_iconify`
  * `key_event` -> `on_key_event`
  * `mouse_position_event` -> `on_mouse_position_event`
  * `mouse_press_event` -> `on_mouse_press_event`
  * `mouse_release_event` -> `on_mouse_release_event`
  * `mouse_drag_event` -> `on_mouse_drag_event`
  * `mouse_scroll_event` -> `on_mouse_scroll_event`
  * `unicode_char_entered` -> `on_unicode_char_entered`
  * `files_dropped_event` -> `on_files_dropped_event`
* Pyrr is now replaced with PyGLM
* imgui is replaced with imgui-bundle
* Numpy version is no longer restricted
* Type annotation improvements
* Python 3.13 support
* Other modernizations in the project

## 2.4.6

* Includes in shaders with quoted paths are now supported
* Renamed incorrect base window method name. `filed_dropped` -> `file_dropped_event`
* Added size setters for headless window
* Added visible setter for all windows
* TextWriter2D should now take viewport size into account
* Loosened up some requirements

## 2.4.5

* Reorganized the project using pyproject.toml
* Upgraded docs dependencies

## 2.4.4

* Added `--backend` option to specify context backend.
  This is mostly for the headless window to enable EGL.
* Window now has a ``backend`` property containing the name of the context backend
* Window now has a ``headless`` boolean property to check if the window is headless.
  This is useful for adding headless only paths in your code.
* Added stencil bits to window framebuffers by default

## 2.4.3

* Fix compatibility with moderngl 5.8.x
* Camera now has keymap support (QWERTY, AZERTY etc)

## 2.4.2

* Allow toggling vsync and runtime for most windows
* Allow rendering with imgui in headless mode
* Fixed a crash when using fullscreen mode with glfw
* Support moving OrbitCamera
* Added SSAO example
* Added `on_generic_event` callback for pygame user events
* Fixed zoom sensitivity getter returning the wrong value
* Fixed several typos
* Bumped several dependencies to reasonable versions

Thanks to @Rafale25, @n3onUser, @erikstrand (Erik Strand),
@sheepman4267 and @dbs4261 (Daniel Simon) for contributions to this release.

## 2.4.1

* Experimental support for ffmpeg capture
* Event callbacks can now be assigned in WindowConfig.__init__
* Initial support for confirming window close (glfw)
* Fixed a crash when closing a pyglet window
* Remove some spammy prints in the text writer

Thanks to @DavideRuzza, @wk39 and @joehalliwell for their
contributions to this release.

## 2.4.0

Python 3.5 is no longer supported from this version.

New Features

* Experimental: New simple 2D text writer
* Various smaller improvements
* F11 now toggles fullscreen mode by default
* Window modules are now fetched from `moderngl_window.WINDOW_CLASSES`
  as a fallback. This is necessary in some environments.
* Absolute paths will now bypass all registered resource directories
  and load the specified file directly.

Bug Fixes

* Varying names can now be passed in when loading a program.
  Since the auto detection of out attributes is far from perfect
  this can be needed for more complex shaders.
* Missing python 3.9 classifier in setup.py
* SDL2 window should now also process since change events
* GLFW: Fixed some incorrect key mappings
* Fixed an issue with timers causing the first frame to have negative frame time
* Fixed a pixel scale issue in the imgui integration. This was especially
  an issue with tiling window managers

## 2.3.0

New Features

* Added a simple Scheduler (Thanks to @Leterax)
* Added support for toggling fullscreen
* Added support for setting window icon
* `TextureDescription` now supports flipping the texture on x and y
* The pyglet window now supports dragging in files
* Added `BaseWindow.convert_window_coordinates` for converting mouse coordinates
* Added more examples

Bug Fixes

* BaseWindow now references WindowConfig using a weakref
* Overriding the timer in `run_window_config` had no effect
* Numpad keys was not mapped correctly in some instances
* Timers should return 0 when not started
* glfw window close callback did now work
* glfw now respects content scaling on windows and X11
* Added some missing methods in docs
* Fixed various doc typos

## 2.2.3

* imgui integration no longer relies on pyopengl
* Bug: Properly parse `out` attributes with layout qualifiers
* Bug: Do not cache system shaders at module level.
  We now cache them in the context to better support multiple windows.
* Bug: OrbitCameraWindow - Fixed radians/degree issue
* Bug: A window can now be closed from inside `render()`

## 2.2.2

* Fixed several issues causing the window close callback not being called
* Fixed incorrect mouse button mapping in mouse drag events

## 2.2.1

* imgui renderer now supports moderngl textures. This opens up for both
  displaying images and animated framebuffer textures into imgui.
* Scene: Fixed several issues related to shader assigning based on material properties.
  This especially affected wavefront/obj files.
* OrbitCamera: Fixed translation issue (@Leterax)
* OrbitCamera: Now using degrees instead of radians (@Leterax)
* Bumped pyglet version to minimum 1.5.6. This version
  solves several issue with window events for MacBooks with Touch Bar

## 2.2.0

* `WindowConfig` now supports overriding the default arugment parser.
  A classmethod `add_arguments` can be implemented to add additional
  arguments. The parsed arguments are available in `self.argv`
* Added in `Scene.draw_wireframe` rendering a scene in wire frame mode
* `Scene.draw_bbox` now support passing in a `color`
* `Scene` should now have better support for all the vertex formats
  wavefront/obj files may have.
* Addded `WindowConfig.clear_color` attribute so uses can control the
  clear color of the screen. The value can be set to `None` to
  disable screen clearing (@Leterax)
* Added `OrbitCamera` (@Leterax)
* Allow setting camera rotation (@Leterax)
* `VAO` should now give better feedback if the buffers and program
  attributes are not compatible
* `ModernGLRenderer` (imgui renderer) should not rely on moderngl-window (@minuJeong)
* `Scene` should now cache default shaders internally so they are not loaded
  for every scene
* Several typos in docs (@dawid-januszkiewicz)
* `WindowConfig.load_compute_shader` missing in docs
* Bumped pygame to `2.0.0.dev10`

Thanks to @Leterax, @minuJeong and @dawid-januszkiewicz for the contributions to this release
and @mtbouchard for input on `WindowConfig` and `Scene` changes.

## 2.1.1

### Improvements

* Optimized the imgui renderer using `ctypes` instead of `numpy` for handling vertex data (@aforren1)
* Added support for ALT key modifier in all window backends and other improvements to key handling (@OKaluza)
* `WindowConfig` now supports a `fullscreen` attribute

Thanks to Alex Forrence (@aforren1) and Owen Kaluza (@OKaluza) for the contributions to this release.

## 2.1.0

New Features

* moderngl and moderngl-window integration for imgui thought the pyimgui project.
  This is fairly experimental and the rendered should probably be moved to the pyimgui project soon

> Dear ImGui is a bloat-free graphical user interface library for C++. It outputs optimized vertex buffers that you can render anytime in your 3D-pipeline enabled application. It is fast, portable, renderer agnostic and self-contained (no external dependencies)

* Compute shader support. `WindowConfig.load_compute_shader` and added `compute_shader` parameter for `ProgramDescription`.
* Shaders now support `#include` up to a maximum of 100 levels
* Added support for gif anim. This can be loaded as a `Texture` or `TextureArray`
* Added support for loading cube maps
* `WindowConfig.run()` shortcut
* Each window backend now has a `name` property so the user can easily detect what window type they are given
* `WindowConfig` now as a `vsync` property so the user can easily control this from python code
* Scene: New methods to find materials and node by name

Slightly Breaking Changes

* All windows now use 0 samples (MSAA) by default. The default `samples = 4` caused way too much issues
  for people with older integrated gpus and when doing headless rendering when multisampling is not supported.

Bug fixes

* Fixed several issues with glft2 scenes and object orientation
* pyglet window: Fixed incorrect mouse position on retina screens and windows
  with pixel ratio > 1.
* sdl2: mouse press/release events was reversed
* pygame2: Fix broken mouse wheel reading
* glfw: Incorrect mapping of BACKSPACE key
* glfw: Fixed an issue not setting vsync properly¨
* headless: We now call `ctx.finish()` in `swap_buffers`
* Shader errors should now report the error line more accurately
* Various typo fixes

## 2.0.5

Improvements

* Windows now has an `exit_key` property that can be used to change
  or disable the exit key. This key is `ESCAPE` by default and can
  be disabled by setting the property to `None`. This is useful
  for users that don't want the default exit key behavior.
* Log consumed glerrors after context creation as warnings

Bug fixes

* Pyglet mouse coordinates was translated wrong in cases were the
  framebuffer size is larger that then window. The mouse position
  should always use window coordinates.
* VAOs should now properly support 64 bit floats / dvec
* VAOs should be better at detecting/ignoring built in attributes
* `Camera.look_at` had broken input validation when passing in a vector
* Various typos in docstrings

## 2.0.4

Resolved an issue with version constraints causing some dependencies to install pre-release versions

## 2.0.3

* Missing `WindowConfig.close` method and support for close callback for all window types
* Bug: KeyboardCamera's matrix is now always returned as a 32bit floats
* Bug: Projection3D's matrix is now always returned as a 32bit floats
* Example cleanup and improvements

## 2.0.2

* Bug: An `INVALID_ENUM` glerror triggered after querying context info is now consumed.

## 2.0.1

Bug fixes

* SDL2 window now allows highdpi framebuffers when available
* pygame2 window should only initialize the display module

## 2.0.0

### Breaking Changes

* `mouse_position_event` signature has changed from `(x, y)` to `(x, y, dx, dy)`.
  This means you will also be getting the relative position change.
* `mouse_drag_event` signature has changed from `(x, y)` to `(x, y, dx, dy)`.
  This means you will also be getting the relative position change.
* `KeyboardCamera.rot_state` now takes dx and dy instead of x and y

### Improvements

* Python 3.8 support (PySide2 will take a few more months. SDL2 has issues on windows)
* Added pygame2 window
* Added window callback `iconify` for all window types that will be called
  when a window is minimized or restored
* Window property `mouse_exclusivity` added for all window types.
  When enabled the mouse cursor is invisible and mouse position changes
  are only reported through the dx and dy values.
* Window property `size` is now assignable for all window types
* Window property `position` is now assignable for all window types
* Window property `title` is now assignable for all window types
* Window property `cursor` is now assignable for all window types
* The `KeyboardCamera` class should now be better at reducing the
  chance of rotation and movement popping
* All windows now properly separate viewport calculations when
  using fixed and free viewport (derived from window size)
* The window `aspect_ratio` property should always return
  the a value based on if the aspect ratio is fixed or free
* Added window `fixed_aspect_ratio` property so users can freely
  control this after window creation

## 1.5.2

* Added window property `position` for getting and setting window position for all window types
* Added window properties: `viewport_size`, `viewport_width`, `viewport_height`
* Upgraded dependency for tkinter window. `pyopengltk>=0.0.3`
* Loosened up most of the requirements
* Bug: Missing call to `tk.destroy()` in tk window

## 1.5.1

* Upgraded dependency for tkinter window. `pyopengltk==0.0.2`.

## 1.5.0

* Added experimental support for tkinter window. Relies on
  Jon Wright's pyopengltk package: <https://github.com/jonwright/pyopengltk>.
  Currently only supports windows and linux, but that might change
  in the future.
* KeyboardCamera: Exposed `mouse_sensitivity`, `velocity` and `projection` attributes
* Various missing docstring and docstring improvements
* Various missing type hints

## 1.4.0

* Added support for mouse_drag events for all window types
* Added support for unicode_char_entered (text input) for all windows
* Added support for mouse wheel events for all window types

## 1.3.0

* Fixed several issue related to python 3.5 support
* Upgraded to pywavefront 1.2.x
* Renamed some modules and classes to better reflect their capabiltities
* Renamed some inconsistent parameter names in the codebase
* Complete overhaul of docstrings in the entire codebase
* Added missing type hints
* Revived the STL loader
* Documentation
* Added `moderngl_window.__version__` attribute

## 1.2.0

* GL errors during window creation is now consumed. This is to avoid confusion when this state is set in the rendering loop.
* Default anisotropy for textures loaders is now 1.0 (disabled, isotropy)
* Mipmaps are no longer generated by default. You must explicitly enable this in parameters.
* WindowConfig.load_texture_2d now exposes more parameters
* WindowConfig.load_texture_array now exposes more parameters
* WindowConfig.load_scene now exposes more parameters
* Texture loaders supports specifying mipmap levels
* Texture loaders supports specifying anisotropy
* VAO wrapper supports normalized float/uint/int
* More tests

## 1.1.0

* Supported buffer formats in the VAO wrapper now matches moderngl better
* VAO wrapper now uses buffer format strings matching moderngl including divisors
* Fixed some logging issues

## 1.0.0

Initial release
