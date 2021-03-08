"""
Follows the standard attributes from GLFT2.0
https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md#meshes
"""


class AttributeNames:
    """Standard buffer/attribute names.

    This works as a lookup for buffer names when creating VAO instances.

    This class can be used directly or an instance of the class can be used with overrides.
    Optionally it can be extended into a new class.
    """

    POSITION = "in_position"
    NORMAL = "in_normal"
    TANGENT = "in_tangent"
    TEXCOORD_0 = "in_texcoord_0"
    TEXCOORD_1 = "in_texcoord_1"
    COLOR_0 = "in_color0"
    JOINTS_0 = "in_joints_0"
    WEIGHTS_0 = "in_weights_0"

    def __init__(
        self,
        position: str = None,
        normal: str = None,
        tangent: str = None,
        texcoord_0: str = None,
        texcoord_1: str = None,
        color_0: str = None,
        joints_0: str = None,
        weights: str = None,
        **kwargs
    ):
        """Override default values.
        All attributes will be set on the instance as upper case strings

        Keyword Args:
                position (str): Name for position buffers/attribute
                normal (str): Name for normal buffer/attribute
                tangent (str): name for tangent buffer/attribute
                texcoord_0 (str): Name for texcoord 0 buffer/attribute
                texcoord_1 (str): Name for texcoord 1 buffer/attribute
                color_0 (str): name for vertex color buffer/attribute
                joints_0 (str): Name for joints buffer/attribute
                weights (str): Name for weights buffer/attribute
        """
        self.apply_values(
            {
                "position": position,
                "normal": normal,
                "tangent": tangent,
                "texcoord_0": texcoord_0,
                "texcoord_1": texcoord_1,
                "color_0": color_0,
                "joints_0": joints_0,
                "weights": weights,
                **kwargs,
            }
        )

    def apply_values(self, kwargs):
        """Only applies attribute values not None"""
        for key, value in kwargs.items():
            if value:
                setattr(self, key.upper(), value)
