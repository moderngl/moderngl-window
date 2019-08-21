
.. py:module:: moderngl_window.context.glfw.window
.. py:currentmodule:: moderngl_window.context.glfw.window

GLFW Window
===========

Methods
-------

.. automethod:: Window.__init__
.. automethod:: Window.init_mgl_context
.. automethod:: Window.is_key_pressed
.. automethod:: Window.close
.. automethod:: Window.use
.. automethod:: Window.clear
.. automethod:: Window.render
.. automethod:: Window.swap_buffers
.. automethod:: Window.resize
.. automethod:: Window.destroy
.. automethod:: Window.set_default_viewport
.. automethod:: Window.print_context_info

Window Specific Methods
-----------------------

.. automethod:: Window.glfw_window_resize_callback
.. automethod:: Window.glfw_mouse_event_callback
.. automethod:: Window.glfw_mouse_button_callback
.. automethod:: Window.glfw_key_event_callback

Attributes
----------

.. autoattribute:: Window.keys
   :annotation:
.. autoattribute:: Window.ctx
.. autoattribute:: Window.fbo
.. autoattribute:: Window.title
.. autoattribute:: Window.gl_version
.. autoattribute:: Window.width
.. autoattribute:: Window.height
.. autoattribute:: Window.size
.. autoattribute:: Window.buffer_size
.. autoattribute:: Window.pixel_ratio
.. autoattribute:: Window.viewport
.. autoattribute:: Window.frames
.. autoattribute:: Window.resizable
.. autoattribute:: Window.fullscreen
.. autoattribute:: Window.config
.. autoattribute:: Window.vsync
.. autoattribute:: Window.aspect_ratio
.. autoattribute:: Window.samples
.. autoattribute:: Window.cursor
.. autoattribute:: Window.render_func
.. autoattribute:: Window.resize_func
.. autoattribute:: Window.key_event_func
.. autoattribute:: Window.mouse_position_event_func
.. autoattribute:: Window.mouse_press_event_func
.. autoattribute:: Window.mouse_release_event_func
.. autoattribute:: Window.is_closing
.. autoattribute:: Window.modifiers
.. autoattribute:: Window.gl_version_code