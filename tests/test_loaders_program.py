from pathlib import Path
import platform
import pytest

import moderngl
from headless import HeadlessTestCase
from moderngl_window import resources
from moderngl_window.meta import ProgramDescription
from moderngl_window.opengl.program import ReloadableProgram
from moderngl_window.exceptions import ImproperlyConfigured

resources.register_dir((Path(__file__).parent / 'fixtures' / 'resources').resolve())


class ProgramLoadersTestCase(HeadlessTestCase):
    window_size = (16, 16)
    aspect_ratio = 1.0

    def test_single(self):
        """Load a single file glsl program"""
        program = resources.programs.load(ProgramDescription(path='programs/white.glsl'))
        self.assertIsInstance(program, moderngl.Program)
        # Ensure attribute is present
        program['in_position']
        self.assertIsInstance(program.extra.get('meta'), ProgramDescription)

    def test_single_feedback(self):
        """Load transform feedback shader"""
        program = resources.programs.load(ProgramDescription(path='programs/feedback.glsl'))
        self.assertIsInstance(program, moderngl.Program)

    def test_single_geometry(self):
        """Load single glsl file with gemotry shader"""
        program = resources.programs.load(ProgramDescription(path='programs/billboards/billboards.glsl'))
        self.assertIsInstance(program, moderngl.Program)

    def test_single_tesselation(self):
        """Load single glsl file with tessellation"""
        program = resources.programs.load(ProgramDescription(path='programs/terrain/terrain.glsl'))
        self.assertIsInstance(program, moderngl.Program)

    def test_single_reloadable(self):
        """Load a single file glsl program as reloadable"""
        program = resources.programs.load(ProgramDescription(path='programs/white.glsl', reloadable=True))
        self.assertIsInstance(program, ReloadableProgram)
        # Ensure attribute is present
        program['in_position']
        self.assertIsInstance(program.extra.get('meta'), ProgramDescription)
        self.assertEqual(program.name, 'programs/white.glsl')
        self.assertIsInstance(program.ctx, moderngl.Context)
        self.assertIsNotNone(program.get('in_position', None))
        self.assertIsNotNone(program.mglo)
        self.assertGreater(program.glo, 0)
        program.subroutines
        program.geometry_input
        program.geometry_output
        program.geometry_vertices
        program._members
        repr(program)

    def test_separate_geometry(self):
        program = resources.programs.load(ProgramDescription(
            vertex_shader="programs/billboards/billboards_vs.glsl",
            geometry_shader="programs/billboards/billboards_gs.glsl",
            fragment_shader="programs/billboards/billboards_fs.glsl",
        ))
        self.assertIsInstance(program, moderngl.Program)

    def test_separate_tesselation(self):
        """Load a more complex tesselation program from separate files"""
        program = resources.programs.load(ProgramDescription(
            vertex_shader="programs/terrain/terrain_vs.glsl",
            tess_control_shader="programs/terrain/terrain_tc.glsl",
            tess_evaluation_shader="programs/terrain/terrain_te.glsl",
            fragment_shader="programs/terrain/terrain_fs.glsl",
        ))
        self.assertIsInstance(program, moderngl.Program)

    def test_separate_relodable(self):
        """Load a more complex tesselation program from separate files"""
        program = resources.programs.load(ProgramDescription(
            vertex_shader="programs/terrain/terrain_vs.glsl",
            tess_control_shader="programs/terrain/terrain_tc.glsl",
            tess_evaluation_shader="programs/terrain/terrain_te.glsl",
            fragment_shader="programs/terrain/terrain_fs.glsl",
            reloadable=True,
        ))
        self.assertIsInstance(program, ReloadableProgram)

    def test_single_not_found(self):
        """Ensure ImproperlyConfigured is raised when shaders are not found"""
        with self.assertRaises(ImproperlyConfigured):
            resources.programs.load(ProgramDescription(path='programs/nonexist.glsl'))

    def test_separate_not_found(self):
        """Ensure ImproperlyConfigured is raised when shaders are not found"""
        with self.assertRaises(ImproperlyConfigured):
            resources.programs.load(ProgramDescription(
                vertex_shader="programs/notfound_vs.glsl",
                geometry_shader="programs/notfound_geo.glsl",
                tess_control_shader="programs/notfound_tc.glsl",
                tess_evaluation_shader="programs/notfound_te.glsl",
                fragment_shader="programs/notfound_fs.glsl",
            ))

    @pytest.mark.skipif(platform.system() == 'Darwin', reason="Compute shader not possible on OSX")
    def test_compute_shader(self):
        """Attempt loading a compute shader"""
        path = 'programs/compute.glsl'
        descr = ProgramDescription(compute_shader=path)
        self.assertEqual(descr.compute_shader, path)
        program = resources.programs.load(descr)
        self.assertIsInstance(program, moderngl.ComputeShader)

    def test_include(self):
        program = resources.programs.load(ProgramDescription(path='programs/include_test.glsl'))
        self.assertIsInstance(program, moderngl.Program)

    def test_varyings_override(self):
        """Specify varyings during program creation"""
        path = 'programs/varyings.glsl'
        descr = ProgramDescription(vertex_shader=path, varyings=["value_1",  "value_2"])
        program = resources.programs.load(descr)
