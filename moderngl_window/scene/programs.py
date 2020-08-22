import os

import numpy
import moderngl
import moderngl_window

from moderngl_window.conf import settings
from moderngl_window.resources import programs
from moderngl_window.meta import ProgramDescription


settings.PROGRAM_DIRS.append(os.path.join(os.path.dirname(__file__), "programs"))


class MeshProgram:
    """
    Describes how a mesh is rendered using a specific shader program
    """

    def __init__(self, program: moderngl.Program = None, **kwargs):
        """Initialize.

        Args:
            program: The moderngl program
        """
        self.program = program

    @property
    def ctx(self):
        """moderngl.Context: The current context"""
        return moderngl_window.ctx()

    def draw(
        self,
        mesh,
        projection_matrix: numpy.ndarray = None,
        model_matrix: numpy.ndarray = None,
        camera_matrix: numpy.ndarray = None,
        time=0.0,
    ):
        """Draw code for the mesh

        Args:
            mesh (Mesh): The mesh to render
        Keyword Args:
            projection_matrix (numpy.ndarray): projection_matrix (bytes)
            model_matrix (numpy.ndarray): view_matrix (bytes)
            camera_matrix (numpy.ndarray): camera_matrix (bytes)
            time (float): The current time
        """
        self.program["m_proj"].write(projection_matrix)
        self.program["m_mv"].write(model_matrix)
        mesh.vao.render(self.program)

    def apply(self, mesh):
        """
        Determine if this ``MeshProgram`` should be applied to the mesh.
        Can return self or some ``MeshProgram`` instance to support dynamic ``MeshProgram`` creation

        Args:
            mesh: The mesh to inspect
        """
        raise NotImplementedError(
            "apply is not implemented. Please override the MeshProgram method"
        )


class VertexColorProgram(MeshProgram):
    """Vertex color program"""

    def __init__(self, program=None, **kwargs):
        super().__init__(program=None)
        self.program = programs.load(
            ProgramDescription(path="scene_default/vertex_color.glsl")
        )

    def draw(
        self,
        mesh,
        projection_matrix=None,
        model_matrix=None,
        camera_matrix=None,
        time=0,
    ):
        self.program["m_proj"].write(projection_matrix)
        self.program["m_model"].write(model_matrix)
        self.program["m_cam"].write(camera_matrix)
        mesh.vao.render(self.program)

    def apply(self, mesh):
        if not mesh.material:
            return None

        if mesh.attributes.get("TEXCOORD_0"):
            return None

        if mesh.attributes.get("COLOR_0"):
            return self

        return None


class ColorLightProgram(MeshProgram):
    """Simple color program with light"""

    def __init__(self, program=None, **kwargs):
        super().__init__(program=None)
        self.program = programs.load(
            ProgramDescription(path="scene_default/color_light.glsl")
        )

    def draw(
        self,
        mesh,
        projection_matrix=None,
        model_matrix=None,
        camera_matrix=None,
        time=0,
    ):

        if mesh.material:
            # if mesh.material.double_sided:
            #     self.ctx.disable(moderngl.CULL_FACE)
            # else:
            #     self.ctx.enable(moderngl.CULL_FACE)

            if mesh.material.color:
                self.program["color"].value = tuple(mesh.material.color)
            else:
                self.program["color"].value = (1.0, 1.0, 1.0, 1.0)

        self.program["m_proj"].write(projection_matrix)
        self.program["m_model"].write(model_matrix)
        self.program["m_cam"].write(camera_matrix)
        mesh.vao.render(self.program)

    def apply(self, mesh):
        if not mesh.material:
            return None

        if not mesh.attributes.get("NORMAL"):
            return None

        return self


class TextureProgram(MeshProgram):
    """Plan textured"""

    def __init__(self, program=None, **kwargs):
        super().__init__(program=None)
        self.program = programs.load(
            ProgramDescription(path="scene_default/texture.glsl")
        )

    def draw(
        self,
        mesh,
        projection_matrix=None,
        model_matrix=None,
        camera_matrix=None,
        time=0,
    ):
        mesh.material.mat_texture.texture.use()
        self.program["m_proj"].write(projection_matrix)
        self.program["m_model"].write(model_matrix)
        self.program["m_cam"].write(camera_matrix)
        mesh.vao.render(self.program)

    def apply(self, mesh):
        if not mesh.material:
            return None

        if mesh.attributes.get("NORMAL"):
            return None

        if not mesh.attributes.get("TEXCOORD_0"):
            return None

        if mesh.attributes.get("COLOR_0"):
            return None

        if mesh.material.mat_texture is not None:
            return self

        return None


class TextureVertexColorProgram(MeshProgram):
    """textred object with vertex color"""

    def __init__(self, program=None, **kwargs):
        super().__init__(program=None)
        self.program = programs.load(
            ProgramDescription(path="scene_default/vertex_color_texture.glsl")
        )

    def draw(
        self,
        mesh,
        projection_matrix=None,
        model_matrix=None,
        camera_matrix=None,
        time=0,
    ):
        mesh.material.mat_texture.texture.use()
        self.program["m_proj"].write(projection_matrix)
        self.program["m_model"].write(model_matrix)
        self.program["m_cam"].write(camera_matrix)
        mesh.vao.render(self.program)

    def apply(self, mesh):
        if not mesh.material:
            return None

        if mesh.attributes.get("NORMAL"):
            return None

        if not mesh.attributes.get("TEXCOORD_0"):
            return None

        if not mesh.attributes.get("COLOR_0"):
            return None

        if mesh.material.mat_texture is not None:
            return self

        return None


class TextureLightProgram(MeshProgram):
    """
    Simple texture program
    """

    def __init__(self, program=None, **kwargs):
        super().__init__(program=None)
        self.program = programs.load(
            ProgramDescription(path="scene_default/texture_light.glsl")
        )

    def draw(
        self,
        mesh,
        projection_matrix=None,
        model_matrix=None,
        camera_matrix=None,
        time=0,
    ):
        # if mesh.material.double_sided:
        #     self.ctx.disable(moderngl.CULL_FACE)
        # else:
        #     self.ctx.enable(moderngl.CULL_FACE)

        mesh.material.mat_texture.texture.use()
        self.program["texture0"].value = 0
        self.program["m_proj"].write(projection_matrix)
        self.program["m_model"].write(model_matrix)
        self.program["m_cam"].write(camera_matrix)
        mesh.vao.render(self.program)

    def apply(self, mesh):
        if not mesh.material:
            return None

        if not mesh.attributes.get("NORMAL"):
            return None

        if not mesh.attributes.get("TEXCOORD_0"):
            return None

        if mesh.material.mat_texture is not None:
            return self

        return None


class TextureLightColorProgram:
    pass


class FallbackProgram(MeshProgram):
    """
    Fallback program only rendering positions in white
    """

    def __init__(self, program=None, **kwargs):
        super().__init__(program=None)
        self.program = programs.load(
            ProgramDescription(path="scene_default/fallback.glsl")
        )

    def draw(
        self,
        mesh,
        projection_matrix=None,
        model_matrix=None,
        camera_matrix=None,
        time=0,
    ):

        self.program["m_proj"].write(projection_matrix)
        self.program["m_model"].write(model_matrix)
        self.program["m_cam"].write(camera_matrix)

        if mesh.material:
            self.program["color"].value = tuple(mesh.material.color[0:3])
        else:
            self.program["color"].value = (1.0, 1.0, 1.0)

        mesh.vao.render(self.program)

    def apply(self, mesh):
        return self
