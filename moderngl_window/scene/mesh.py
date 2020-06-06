from pyrr import matrix44
import numpy


class Mesh:
    """Mesh info and geometry"""

    def __init__(self, name, vao=None, material=None, attributes=None, bbox_min=None, bbox_max=None):
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
        self.mesh_program = None

    def draw(self, projection_matrix=None, model_matrix=None, camera_matrix=None, time=0.0):
        """Draw the mesh using the assigned mesh program

        Keyword Args:
            projection_matrix (bytes): projection_matrix
            view_matrix (bytes): view_matrix
            camera_matrix (bytes): camera_matrix
        """
        if self.mesh_program:
            self.mesh_program.draw(
                self,
                projection_matrix=projection_matrix,
                model_matrix=model_matrix,
                camera_matrix=camera_matrix,
                time=time
            )

    def draw_bbox(self, proj_matrix, model_matrix, cam_matrix, program, vao):
        """Renders the bounding box for this mesh.

        Args:
            proj_matrix: Projection matrix
            model_matrix: View/model matrix
            cam_matrix: Camera matrix
            program: The moderngl.Program rendering the bounding box
            vao: The vao mesh for the bounding box
        """
        program["m_proj"].write(proj_matrix)
        program["m_model"].write(model_matrix)
        program["m_cam"].write(cam_matrix)
        program["bb_min"].write(self.bbox_min.astype('f4').tobytes())
        program["bb_max"].write(self.bbox_max.astype('f4').tobytes())
        vao.render(program)

    def draw_wireframe(self, proj_matrix, model_matrix, program):
        """Render the mesh as wireframe.

            proj_matrix: Projection matrix
            model_matrix: View/model matrix
            program: The moderngl.Program rendering the wireframe
        """
        program["m_proj"].write(proj_matrix)
        program["m_model"].write(model_matrix)
        self.vao.render(program)

    def add_attribute(self, attr_type, name, components):
        """
        Add metadata about the mesh
        :param attr_type: POSITION, NORMAL etc
        :param name: The attribute name used in the program
        :param components: Number of floats
        """
        self.attributes[attr_type] = {"name": name, "components": components}

    def calc_global_bbox(self, view_matrix, bbox_min, bbox_max):
        """Calculates the global bounding.

        Args:
            view_matrix: View matrix
            bbox_min: xyz min
            bbox_max: xyz max
        Returns:
            bbox_min, bbox_max: Combined bbox
        """
        # Copy and extend to vec4
        bb1 = numpy.append(self.bbox_min[:], 1.0).astype('f4')
        bb2 = numpy.append(self.bbox_max[:], 1.0).astype('f4')

        # Transform the bbox values
        bmin = matrix44.apply_to_vector(view_matrix, bb1),
        bmax = matrix44.apply_to_vector(view_matrix, bb2),
        bmin = numpy.asarray(bmin, dtype='f4')[0]
        bmax = numpy.asarray(bmax, dtype='f4')[0]

        # If a rotation happened there is an axis change and we have to ensure max-min is positive
        for i in range(3):
            if bmax[i] - bmin[i] < 0:
                bmin[i], bmax[i] = bmax[i], bmin[i]

        if bbox_min is None or bbox_max is None:
            return bmin[0:3], bmax[0:3]

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

    def has_uvs(self, layer=0) -> bool:
        """
        Returns:
            bool: Does the mesh have texture coordinates?
        """
        return "TEXCOORD_{}".format(layer) in self.attributes
