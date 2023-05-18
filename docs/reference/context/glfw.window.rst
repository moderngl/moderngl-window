
.. py:module:: moderngl_window.context.glfw.window
.. py:currentmodule:: moderngl_window.context.glfw.window

glfw.Window
===========

Methods
-------

.. automethod:: Window.__init__
.. automethod:: Window.init_mgl_context
.. automethod:: Window.is_key_pressed
.. automethod:: Window.set_icon
.. automethod:: Window.close
.. automethod:: Window.use
.. automethod:: Window.clear
.. automethod:: Window.render
.. automethod:: Window.swap_buffers
.. automethod:: Window.resize
.. automethod:: Window.destroy
.. automethod:: Window.set_default_viewport
.. automethod:: Window.print_context_info
.. automethod:: Window.convert_window_coordinates

Attributes
----------

.. autoattribute:: Window.name
.. autoattribute:: Window.keys
   :annotation:
.. autoattribute:: Window.ctx
.. autoattribute:: Window.backend
.. autoattribute:: Window.headless
.. autoattribute:: Window.fbo
.. autoattribute:: Window.title
.. autoattribute:: Window.exit_key
.. autoattribute:: Window.fullscreen_key
.. autoattribute:: Window.gl_version
.. autoattribute:: Window.width
.. autoattribute:: Window.height
.. autoattribute:: Window.size
.. autoattribute:: Window.position
.. autoattribute:: Window.fullscreen
.. autoattribute:: Window.buffer_width
.. autoattribute:: Window.buffer_height
.. autoattribute:: Window.buffer_size
.. autoattribute:: Window.pixel_ratio
.. autoattribute:: Window.viewport
.. autoattribute:: Window.viewport_size
.. autoattribute:: Window.viewport_width
.. autoattribute:: Window.viewport_height
.. autoattribute:: Window.frames
.. autoattribute:: Window.resizable
.. autoattribute:: Window.close_func
.. autoattribute:: Window.fullscreen
.. autoattribute:: Window.config
.. autoattribute:: Window.vsync
.. autoattribute:: Window.aspect_ratio
.. autoattribute:: Window.fixed_aspect_ratio
.. autoattribute:: Window.samples
.. autoattribute:: Window.cursor
.. autoattribute:: Window.mouse_exclusivity
.. autoattribute:: Window.render_func
.. autoattribute:: Window.resize_func
.. autoattribute:: Window.iconify_func
.. autoattribute:: Window.key_event_func
.. autoattribute:: Window.on_generic_event_func
.. autoattribute:: Window.mouse_position_event_func
.. autoattribute:: Window.mouse_press_event_func
.. autoattribute:: Window.mouse_release_event_func
.. autoattribute:: Window.mouse_drag_event_func
.. autoattribute:: Window.mouse_scroll_event_func
.. autoattribute:: Window.unicode_char_entered_func
.. autoattribute:: Window.files_dropped_event_func
.. autoattribute:: Window.is_closing
.. autoattribute:: Window.mouse
.. autoattribute:: Window.mouse_states
.. autoattribute:: Window.modifiers
.. autoattribute:: Window.gl_version_code

Window Specific Methods
-----------------------

.. automethod:: Window.glfw_window_resize_callback
.. automethod:: Window.glfw_mouse_event_callback
.. automethod:: Window.glfw_mouse_button_callback
.. automethod:: Window.glfw_mouse_scroll_callback
.. automethod:: Window.glfw_key_event_callback
.. automethod:: Window.glfw_char_callback
.. automethod:: Window.glfw_cursor_enter
.. automethod:: Window.glfw_window_focus
.. automethod:: Window.glfw_window_iconify
.. automethod:: Window.glfw_window_close
