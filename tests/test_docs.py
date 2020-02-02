"""
Documentation testing
Inspired by:
https://github.com/cprogrammer1994/ModernGL/blob/master/tests/test_documentation.py
by Szabolcs Dombi
This version is simplified:
* Only test if the attribute or method is present in the class. Function parameters are not inspected.
* Include ignore pattern in the implemented set
"""
import os
import re
import sys
import types
import unittest
from unittest.mock import MagicMock

from moderngl_window.utils import module_loading

# Mock modules
class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()


MOCK_MODULES = [
    'glfw',
    'sdl2',
    'sdl2.ext',
    'sdl2.video',
    'pyglet',
    'pyglet.window',
    'PyQt5',
    'PyQt5.QtCore',
    'QtCore',
    'QtOpenGL',
    'QtWidgets',
    'PySide2',
    'PySide2.QtCore',
]

sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)


class TestCase(unittest.TestCase):
    """
    Test reference docs
    """
    def validate(self, filename, module, classname=None, ignore=None):
        """
        Finds all automethod and autoattribute statements in an rst file
        comparing them to the attributes found in the actual class
        """
        if ignore is None:
            ignore = []

        with open(os.path.normpath(os.path.join('docs', 'reference', filename))) as f:
            docs = f.read()

        module = module_loading.import_module(module)

        # Inspect class
        if classname:
            methods = re.findall(r'^\.\. automethod:: ([^\(\n]+)', docs, flags=re.M)
            attributes = re.findall(r'^\.\. autoattribute:: ([^\n]+)', docs, flags=re.M)

            documented = set(filter(lambda x: x.startswith(classname), [a for a in methods] + attributes))
            implemented = set(classname + '.' + x for x in dir(getattr(module, classname))
                              if not x.startswith('_') or x == '__init__')
            ignored = set(classname + '.' + x for x in ignore)
        # Inspect module
        else:
            # Only inspect functions for now
            functions = re.findall(r'^\.\. autofunction:: ([^\(\n]+)', docs, flags=re.M)
            documented = set(functions)
            ignored = set(ignore)
            implemented = set(func for func in dir(module) if isinstance(getattr(module, func), types.FunctionType))

        self.assertSetEqual(implemented - documented - ignored, set(), msg='Implemented but not Documented')
        self.assertSetEqual(documented - implemented - ignored, set(), msg='Documented but not Implemented')

    def test_moderngl_window(self):
        self.validate(
            'moderngl_window.rst',
            'moderngl_window',
            ignore=['valid_window_size', 'valid_window_size_multiplier', 'import_string', 'valid_bool'],
        )

    def test_settings(self):
        self.validate('settings.conf.settings.rst', 'moderngl_window.conf', 'Settings', [])

    # --- context ---

    def test_context_base_window(self):
        self.validate('context/basewindow.rst', 'moderngl_window.context.base.window', 'BaseWindow')

    def test_context_glfw_window(self):
        self.validate('context/glfw.window.rst', 'moderngl_window.context.glfw.window', 'Window')

    def test_context_headless_window(self):
        self.validate('context/headless.window.rst', 'moderngl_window.context.headless.window', 'Window')

    def test_context_pyglet_window(self):
        self.validate('context/pyglet.window.rst', 'moderngl_window.context.pyglet.window', 'Window')

    def test_context_pyqt5_window(self):
        self.validate('context/pyqt5.window.rst', 'moderngl_window.context.pyqt5.window', 'Window')

    @unittest.skipIf(sys.version_info >= (3, 8, 0), reason="pyside2 not supported in py38 yet")
    def test_context_pyside2_window(self):
        self.validate('context/pyside2.window.rst', 'moderngl_window.context.pyside2.window', 'Window')

    def test_context_sdl2_window(self):
        self.validate('context/sdl2.window.rst', 'moderngl_window.context.sdl2.window', 'Window')

    # --- geometry ---

    def test_geometry(self):
        self.validate('geometry.rst', 'moderngl_window.geometry')

    # --- Loaders ---

    def test_loaders_base(self):
        self.validate('loaders/base.rst', 'moderngl_window.loaders.base', 'BaseLoader')

    # --- Loaders : Texture ---

    def test_loaders_t2d(self):
        self.validate('loaders/t2d.rst', 'moderngl_window.loaders.texture.t2d', 'Loader')

    def test_loaders_array(self):
        self.validate('loaders/array.rst', 'moderngl_window.loaders.texture.array', 'Loader')

    # --- Loaders : Scene ---

    def test_loaders_wavefront(self):
        self.validate('loaders/wavefront.rst', 'moderngl_window.loaders.scene.wavefront', 'Loader')

    def test_loaders_gltf(self):
        self.validate('loaders/gltf2.rst', 'moderngl_window.loaders.scene.gltf2', 'Loader')

    def test_loaders_stl(self):
        self.validate('loaders/wavefront.rst', 'moderngl_window.loaders.scene.stl', 'Loader')

    # --- Loaders : Program ---

    def test_loader_single(self):
        self.validate('loaders/single.rst', 'moderngl_window.loaders.program.single', 'Loader')

    def test_loader_separate(self):
        self.validate('loaders/separate.rst', 'moderngl_window.loaders.program.separate', 'Loader')

    # --- Loaders : Data ---

    def test_loader_text(self):
        self.validate('loaders/text.rst', 'moderngl_window.loaders.data.text', 'Loader')

    def test_loader_json(self):
        self.validate('loaders/json.rst', 'moderngl_window.loaders.data.json', 'Loader')

    def test_loader_binary(self):
        self.validate('loaders/binary.rst', 'moderngl_window.loaders.data.binary', 'Loader')

    # --- Meta ---

    def test_meta_base(self):
        self.validate('meta/base.rst', 'moderngl_window.meta.base', 'ResourceDescription')

    def test_meta_texture(self):
        self.validate('meta/texture.rst', 'moderngl_window.meta.texture', 'TextureDescription')

    def test_meta_program(self):
        self.validate('meta/program.rst', 'moderngl_window.meta.program', 'ProgramDescription')

    def test_meta_scene(self):
        self.validate('meta/scene.rst', 'moderngl_window.meta.scene', 'SceneDescription')

    def test_meta_data(self):
        self.validate('meta/data.rst', 'moderngl_window.meta.data', 'DataDescription')

    # --- Finders ---

    def test_finders_base(self):
        self.validate('finders/base.rst', 'moderngl_window.finders.base', 'BaseFilesystemFinder')

    def test_finders_texture(self):
        self.validate('finders/texture.rst', 'moderngl_window.finders.texture', 'FilesystemFinder')

    def test_finders_program(self):
        self.validate('finders/program.rst', 'moderngl_window.finders.program', 'FilesystemFinder')

    def test_finders_scene(self):
        self.validate('finders/scene.rst', 'moderngl_window.finders.scene', 'FilesystemFinder')

    def test_finders_data(self):
        self.validate('finders/data.rst', 'moderngl_window.finders.data', 'FilesystemFinder')

    # --- opengl ---

    def test_opengl_projection3d(self):
        self.validate('opengl/projection.rst', 'moderngl_window.opengl.projection', 'Projection3D')

    def test_opengl_vao(self):
        self.validate('opengl/vao.rst', 'moderngl_window.opengl.vao', 'VAO')

    # --- resources ---

    def test_resources_base(self):
        self.validate('resources/base.rst', 'moderngl_window.resources.base', 'BaseRegistry')

    def test_resources_data(self):
        self.validate('resources/data.rst', 'moderngl_window.resources.data', 'DataFiles')

    def test_resources_textures(self):
        self.validate('resources/textures.rst', 'moderngl_window.resources.textures', 'Textures')

    def test_resources_programs(self):
        self.validate('resources/programs.rst', 'moderngl_window.resources.programs', 'Programs')

    def test_resources_scenes(self):
        self.validate('resources/scenes.rst', 'moderngl_window.resources.scenes', 'Scenes')

    # --- timers ---

    def test_timers_base(self):
        self.validate('timers/base.rst', 'moderngl_window.timers.base', 'BaseTimer')

    def test_timers_clock(self):
        self.validate('timers/clock.rst', 'moderngl_window.timers.clock', 'Timer')

    # -- Scene ---

    def test_scene_camera(self):
        self.validate('scene/camera.rst', 'moderngl_window.scene', 'Camera')

    def test_scene_keyboardcamera(self):
        self.validate('scene/keyboardcamera.rst', 'moderngl_window.scene', 'KeyboardCamera')

    def test_scene_scene(self):
        self.validate('scene/scene.rst', 'moderngl_window.scene', 'Scene')

    def test_scene_node(self):
        self.validate('scene/node.rst', 'moderngl_window.scene', 'Node')

    def test_scene_mesh(self):
        self.validate('scene/mesh.rst', 'moderngl_window.scene', 'Mesh')

    def test_scene_material(self):
        self.validate('scene/material.rst', 'moderngl_window.scene', 'Material')

    def test_scene_material_texture(self):
        self.validate('scene/materialtexture.rst', 'moderngl_window.scene', 'MaterialTexture')

    def test_scene_meshprogram(self):
        self.validate('scene/meshprogram.rst', 'moderngl_window.scene', 'MeshProgram')
