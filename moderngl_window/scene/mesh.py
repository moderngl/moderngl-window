from typing import TYPE_CHECKING, Any, Optional

import glm
import moderngl

from moderngl_window.opengl.vao import VAO

from .material import Material

if TYPE_CHECKING:
    from .programs import MeshProgram


class Mesh:
    """Mesh info and geometry"""

    def __init__(
        self,
        name: str,
        vao: Optional[VAO] = None,
        material: Optional[Material] = None,
        attributes: Optional[dict[str, Any]] = None,
        bbox_min: glm.vec3 = glm.vec3(),
        bbox_max: glm.vec3 = glm.vec3(),
    ) -> None:
        """Initialize mesh.

        Args:
            name (str): name of the mesh
        Keyword Args:
            vao (VAO): geometry
            material (Material): material for the mesh
            attributes (dict): Details info about each mesh attribute (dict)
            bbox_min: xyz min values
            bbox_max: xyz max values

        Attributes example::

            {
                "NORMAL": {"name": "in_normal", "components": 3, "type": GL_FLOAT},
                "POSITION": {"name": "in_position", "components": 3, "type": GL_FLOAT}
            }
        """
        self.name = name
        self.vao = vao
        self.material = material
        self.attributes = attributes or {}
        self.bbox_min = bbox_min
        self.bbox_max = bbox_max
        self.mesh_program: Optional["MeshProgram"] = None

    def draw(
        self,
        projection_matrix: glm.mat4,
        model_matrix: glm.mat4,
        camera_matrix: glm.mat4,
        time: float = 0.0,
    ) -> None:
        """Draw the mesh using the assigned mesh program

        Keyword Args:
            projection_matrix (bytes): projection_matrix
            view_matrix (bytes): view_matrix
            camera_matrix (bytes): camera_matrix
        """
        if self.mesh_program is not None:
            self.mesh_program.draw(
                self,
                projection_matrix=projection_matrix,
                model_matrix=model_matrix,
                camera_matrix=camera_matrix,
                time=time,
            )

    def draw_bbox(
        self,
        proj_matrix: glm.mat4,
        model_matrix: glm.mat4,
        cam_matrix: glm.mat4,
        program: moderngl.Program,
        vao: VAO,
    ) -> None:
        """Renders the bounding box for this mesh.

        Args:
            proj_matrix: Projection matrix
            model_matrix: View/model matrix
            cam_matrix: Camera matrix
            program: The moderngl.Program rendering the bounding box
            vao: The vao mesh for the bounding box
        """
        program["m_proj"].write(proj_matrix.to_bytes())
        program["m_model"].write(model_matrix.to_bytes())
        program["m_cam"].write(cam_matrix.to_bytes())
        program["bb_min"].write(self.bbox_min.to_bytes())
        program["bb_max"].write(self.bbox_max.to_bytes())
        vao.render(program)

    def draw_wireframe(
        self, proj_matrix: glm.mat4, model_matrix: glm.mat4, program: moderngl.Program
    ) -> None:
        """Render the mesh as wireframe.

        proj_matrix: Projection matrix
        model_matrix: View/model matrix
        program: The moderngl.Program rendering the wireframe
        """
        assert self.vao is not None, "Can not draw the wireframe, vao is empty"
        program["m_proj"].write(proj_matrix.to_bytes())
        program["m_model"].write(model_matrix.to_bytes())
        self.vao.render(program)

    def add_attribute(self, attr_type: str, name: str, components: int) -> None:
        """
        Add metadata about the mesh
        :param attr_type: POSITION, NORMAL etc
        :param name: The attribute name used in the program
        :param components: Number of floats
        """
        self.attributes[attr_type] = {"name": name, "components": components}

    def calc_global_bbox(
        self, view_matrix: glm.mat4, bbox_min: glm.vec3 | None, bbox_max: glm.vec3 | None
    ) -> tuple[glm.vec3, glm.vec3]:
        """Calculates the global bounding.

        Args:
            view_matrix: View matrix
            bbox_min: xyz min
            bbox_max: xyz max
        Returns:
            bbox_min, bbox_max: Combined bbox
        """
        # Copy and extend to vec4
        bb1 = glm.vec4(self.bbox_min, 1.0)
        bb2 = glm.vec4(self.bbox_max, 1.0)

        # Transform the bbox values
        bmin = view_matrix * bb1
        bmax = view_matrix * bb2

        # If a rotation happened there is an axis change and we have to ensure max-min is positive
        for i in range(3):
            if bmax[i] - bmin[i] < 0:
                bmin[i], bmax[i] = bmax[i], bmin[i]

        if bbox_min is None or bbox_max is None:
            return (glm.vec3(bmin.x, bmin.y, bmin.z), glm.vec3(bmax.x, bmax.y, bmax.z))

        for i in range(3):
            bbox_min[i] = min(bbox_min[i], bmin[i])

        for i in range(3):
            bbox_max[i] = max(bbox_max[i], bmax[i])

        return bbox_min, bbox_max

    def has_normals(self) -> bool:
        """
        Returns:
            bool: Does the mesh have a normals?
        """
        return "NORMAL" in self.attributes

    def has_uvs(self, layer: int = 0) -> bool:
        """
        Returns:
            bool: Does the mesh have texture coordinates?
        """
        return "TEXCOORD_{}".format(layer) in self.attributes
