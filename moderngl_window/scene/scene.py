"""
Wrapper for a loaded scene with properties.
"""
from pyrr import matrix44, vector3

from demosys import context, geometry
from demosys.resources import programs
from demosys.resources.meta import ProgramDescription

from .programs import (ColorProgram, FallbackProgram, MeshProgram,
                       TextureProgram)


class Scene:
    """Generic scene"""
    def __init__(self, name, mesh_programs=None, **kwargs):
        """
        :param name: Unique name or path for the scene
        :param mesh_programs: List of MeshPrograms to apply to the scene
        :param loader: Loader class for the scene if relevant
        """
        self.name = name
        self.root_nodes = []

        # References resources in the scene
        self.nodes = []
        self.materials = []
        self.meshes = []
        self.cameras = []

        self.bbox_min = None
        self.bbox_max = None
        self.diagonal_size = 1.0

        self.bbox_vao = geometry.bbox()
        self.bbox_program = programs.load(ProgramDescription(
            label='scene_default/bbox.glsl',
            path='scene_default/bbox.glsl'))

        self._view_matrix = matrix44.create_identity()

    @property
    def ctx(self):
        return context.ctx()

    @property
    def view_matrix(self):
        return self._view_matrix

    @view_matrix.setter
    def view_matrix(self, value):
        self._view_matrix = value.astype('f4')
        for node in self.root_nodes:
            node.calc_view_mat(self._view_matrix)

    def draw(self, projection_matrix=None, camera_matrix=None, time=0):
        """
        Draw all the nodes in the scene

        :param projection_matrix: projection matrix (bytes)
        :param camera_matrix: camera_matrix (bytes)
        :param time: The current time
        """
        projection_matrix = projection_matrix.astype('f4').tobytes()
        camera_matrix = camera_matrix.astype('f4').tobytes()

        for node in self.root_nodes:
            node.draw(
                projection_matrix=projection_matrix,
                camera_matrix=camera_matrix,
                time=time,
            )

        self.ctx.clear_samplers(0, 4)

    def draw_bbox(self, projection_matrix=None, camera_matrix=None, all=True):
        """Draw scene and mesh bounding boxes"""
        projection_matrix = projection_matrix.astype('f4').tobytes()
        camera_matrix = camera_matrix.astype('f4').tobytes()

        # Scene bounding box
        self.bbox_program["m_proj"].write(projection_matrix)
        self.bbox_program["m_view"].write(self._view_matrix.astype('f4').tobytes())
        self.bbox_program["m_cam"].write(camera_matrix)
        self.bbox_program["bb_min"].write(self.bbox_min.astype('f4').tobytes())
        self.bbox_program["bb_max"].write(self.bbox_max.astype('f4').tobytes())
        self.bbox_program["color"].value = (1.0, 0.0, 0.0)
        self.bbox_vao.render(self.bbox_program)

        if not all:
            return

        # Draw bounding box for children
        for node in self.root_nodes:
            node.draw_bbox(projection_matrix, camera_matrix, self.bbox_program, self.bbox_vao)

    def apply_mesh_programs(self, mesh_programs=None):
        """Applies mesh programs to meshes"""
        if not mesh_programs:
            mesh_programs = [ColorProgram(), TextureProgram(), FallbackProgram()]

        for mesh in self.meshes:
            for mp in mesh_programs:
                instance = mp.apply(mesh)
                if instance is not None:
                    if isinstance(instance, MeshProgram):
                        mesh.mesh_program = mp
                        break
                    else:
                        raise ValueError("apply() must return a MeshProgram instance, not {}".format(type(instance)))

            if not mesh.mesh_program:
                print("WARING: No mesh program applied to '{}'".format(mesh.name))

    def calc_scene_bbox(self):
        """Calculate scene bbox"""
        bbox_min, bbox_max = None, None
        for node in self.root_nodes:
            bbox_min, bbox_max = node.calc_global_bbox(
                matrix44.create_identity(),
                bbox_min,
                bbox_max
            )

        self.bbox_min = bbox_min
        self.bbox_max = bbox_max

        self.diagonal_size = vector3.length(self.bbox_max - self.bbox_min)

    def prepare(self):
        self.apply_mesh_programs()
        self.view_matrix = matrix44.create_identity()

    def destroy(self):
        """Destroy the scene data and deallocate buffers"""
        for mesh in self.meshes:
            mesh.vao.release()

    def __str__(self):
        return "<Scene: {}>".format(self.name)

    def __repr__(self):
        return str(self)
