"""
Mesh class containing geometry information
"""
from pyrr import matrix44
import numpy


class Mesh:
    """Mesh info and geometry"""

    def __init__(self, name, vao=None, material=None, attributes=None, bbox_min=None, bbox_max=None):
        """
        :param name: Name of the mesh
        :param vao: VAO
        :param material: Material
        :param attributes: Details info about each mesh attribute (dict)
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

    def draw(self, projection_matrix=None, view_matrix=None, camera_matrix=None, time=0):
        """
        Draw the mesh using the assigned mesh program

        :param projection_matrix: projection_matrix (bytes)
        :param view_matrix: view_matrix (bytes)
        :param camera_matrix: camera_matrix (bytes)
        """
        if self.mesh_program:
            self.mesh_program.draw(
                self,
                projection_matrix=projection_matrix,
                view_matrix=view_matrix,
                camera_matrix=camera_matrix,
                time=time
            )

    def draw_bbox(self, proj_matrix, view_matrix, cam_matrix, program, vao):
        program["m_proj"].write(proj_matrix)
        program["m_view"].write(view_matrix)
        program["m_cam"].write(cam_matrix)
        program["bb_min"].write(self.bbox_min.astype('f4').tobytes())
        program["bb_max"].write(self.bbox_max.astype('f4').tobytes())
        program["color"].value = (0.75, 0.75, 0.75)
        vao.render(program)

    def add_attribute(self, attr_type, name, components):
        """
        Add metadata about the mesh
        :param attr_type: POSITION, NORMAL etc
        :param name: The attribute name used in the program
        :param components: Number of floats
        """
        self.attributes[attr_type] = {"name": name, "components": components}

    def calc_global_bbox(self, view_matrix, bbox_min, bbox_max):
        # Copy and extend to vec4
        bb1 = numpy.append(self.bbox_min[:], 1.0)
        bb2 = numpy.append(self.bbox_max[:], 1.0)

        # Transform the bbox values
        bmin = matrix44.apply_to_vector(view_matrix, bb1),
        bmax = matrix44.apply_to_vector(view_matrix, bb2),
        bmin = numpy.asarray(bmin)[0]
        bmax = numpy.asarray(bmax)[0]

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

    def has_normals(self):
        return "NORMAL" in self.attributes

    def has_uvs(self, layer=0):
        return "TEXCOORD_{}".format(layer) in self.attributes
