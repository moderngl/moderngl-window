
The Resource System
===================

Resource Types
--------------

The resource system has four different resource
types/categories it can load.

* **Programs** : Shader programs (vertex, geometry, fragment, tessellation,
  compute)
* **Textures** : Textures of all different variations
* **Scenes**: Wavefront, GLTF2 and STL scenes/objects
* **Data**: A generic "lane" for everything else

Each of these resource categories have separate search
directories, one or multiple loader classes and a
:py:class:`~moderngl_window.meta.base.ResourceDescription`
class we use to describe the resource we are loading
with all its parameters.

Resource Paths
--------------

Resources are loaded using relative paths. These paths
are relative to one or multiple search directories
we register using the :py:mod:`~moderngl_window.resources`
module.

For simple usage were we have one or multiple resource
directories with mixed resource types (programs, textures
etc.) we can use the simplified version,
:py:func:`~moderngl_window.resources.register_dir`.

.. code:: python

    from pathlib import Path
    from moderngl_window import resources

    # pathlib.Path (recommended)
    resources.register_dir(Path('absoulte/path/using/pathlib'))

    # Strings and/or os.path
    resources.register_dir('absolute/string/path')

A resource finder system will scan through the registered
directories in the order they were added loading the
first resource found.

For more advanced usage were resources of different types
are separated we can register resource type specific search
directories:

* :py:func:`~moderngl_window.resources.register_program_dir`
* :py:func:`~moderngl_window.resources.register_texture_dir`
* :py:func:`~moderngl_window.resources.register_scene_dir`
* :py:func:`~moderngl_window.resources.register_data_dir`

This can be handy when dealing with larger quantities of
files.
These search directories are stored in the
:py:class:`~moderngl_window.conf.Settings` instance
and can for example be temporarily altered if needed.
This means you can separate local and global resources
in more complex situations. It could even be used to
support themes by promoting a theme directory overriding
global/default resources or some default theme directory.

Resource Descriptions
---------------------

Resource descriptions are basically just classes
acting as bags of attributes describing the resource
we are requesting. We have four standard classes.

* :py:class:`~moderngl_window.meta.program.ProgramDescription`
* :py:class:`~moderngl_window.meta.texture.TextureDescription`
* :py:class:`~moderngl_window.meta.scene.SceneDescription`
* :py:class:`~moderngl_window.meta.data.DataDescription`

Example::

    from moderngl_window.meta import TextureDescription

    # We are aiming to load wood.png horizontally flipped
    # with generated mipmaps and high anisotropic filtering.
    TextureDescription(
        path='wood.png',
        flip=True,
        mipmap=True,
        anisotropy=16.0,
    )

New resource description classes can be created
by extending the base
:py:class:`~moderngl_window.meta.base.ResourceDescription` class.
This is not uncommon when for example making a new loader class.

Loading Resources
-----------------

Now that we know about the different resoure categories,
search paths and resource descriptions, we're ready to
actually load something.

.. code:: python

    from moderngl_window import resources
    from moderngl_window.meta import (
        TextureDescription,
        ProgramDescription,
        SceneDescription,
        DataDescription,
    )

    texture = resource.textures.load(TextureDescription(path='wood.png')
    program = resource.programs.load(ProgramDescription(path='fun.glsl')
    program = resource.programs.load(ProgramDescription(
        vertex_shader='sphere_vert.glsl',
        geometry_shader='sphere_geo.glsl',
        fragment_shader='sphere_fs.glsl'
    ))
    scene = resources.load(SceneDescription(path="city.gltf')
    text = resources.load(DataDescription(path='notes.txt')
    config_dict = resources.load(DataDescription(path='config.json')
    data = resources.load(DataDescription(path='data.bin', kind='binary)

For more information about supported parameters see the api documenation.
