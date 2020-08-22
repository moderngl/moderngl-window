"""
Notes from moderngl:

The vao_content is a list of 3-tuples (buffer, format, attribs)
the format can have an empty or '/v', '/i', '/r' ending.
'/v' attributes are the default
'/i` attributes are per instance attributes
'/r' attributes are per render (like a uniform)
Example:
    vao_content = [
        (self.position_vertex_buffer, '2f', 'in_vert'),
        (self.color_buffer, '3f', 'in_color'),
        (self.pos_scale_buffer, '2f 1f/i', 'in_pos', 'in_scale'),
    ]
"""
import re
from functools import lru_cache
from typing import List

VALID_DIVISORS = ["v", "i", "r"]


class BufferFormat:
    def __init__(
        self,
        format_string: str,
        components: int,
        bytes_per_component: int,
        per_instance=False,
    ):
        """
        Args:
            format_string (str): moderngl format string
            components (int): components
            byte_size (int): bytes per component
            per_instance (bool): Instanced attribute
        """
        self.format = format_string
        self.components = components
        self.bytes_per_component = bytes_per_component
        self.per_instance = per_instance

    @property
    def bytes_total(self) -> int:
        """int: total byte size if this type"""
        return self.components * self.bytes_per_component

    def pad_str(self) -> str:
        """Padding string used my moderngl in interleaved buffers"""
        return "{}x{}".format(self.components, self.bytes_per_component)

    def __str__(self) -> str:
        return "<BufferFormat {} components={} bytes_per_component={}>".format(
            self.format, self.components, self.bytes_per_component
        )

    def __repr__(self) -> str:
        return str(self)


@lru_cache(maxsize=500)
def attribute_format(attr_format: str) -> BufferFormat:
    """Look up info about an attribute format.

    Translate the format into a BufferFormat instance
    containing things like byte size and components

    Args:
        buffer_format (str): Format of an attribute
    Returns:
        BufferFormat instance
    """
    if not attr_format:
        raise ValueError("Cannot resolve buffer format: '{}'".format(attr_format))

    parts = attr_format.split("/")

    # Parse out divisor if present
    # Examples: 3f/i, 3f/v
    fmt = parts[0]
    divisor = ""
    if len(parts) > 1:
        divisor = parts[1]
        if divisor not in VALID_DIVISORS:
            raise ValueError(
                "Invalid attribute divisor '{}' in '{}'".format(divisor, buffer_format)
            )

    # Parse out out component count and actual format
    parts = re.split(r"([fiudn])", fmt)
    components = 1
    if parts[0].isalnum():
        components = int(parts[0])
        bformat = fmt[len(parts[0]) :]
    else:
        bformat = fmt

    # Construct specific buffer format
    fmt_info = buffer_format(bformat)
    return BufferFormat(
        "{}{}{}".format(components, bformat, "/{}".format(divisor) if divisor else ""),
        components,
        fmt_info.bytes_per_component,
        per_instance=divisor == "i",
    )


def parse_attribute_formats(frmt: str) -> List[BufferFormat]:
    return [attribute_format(attr) for attr in frmt.split()]


def buffer_format(frmt: str) -> BufferFormat:
    """Look up info about a buffer format type

    Args:
        frmt (str): format string such as 'f', 'i' and 'u'
    Returns:
        BufferFormat instance
    """
    try:
        return BUFFER_FORMATS[frmt]
    except KeyError:
        raise ValueError(
            "Buffer format '{}' unknown. Valid formats: {}".format(
                frmt, BUFFER_FORMATS.keys()
            )
        )


BUFFER_FORMATS = {
    # Floats
    "f": BufferFormat("f", 1, 4),
    "f1": BufferFormat("f1", 1, 1),
    "f2": BufferFormat("f2", 1, 2),
    "f4": BufferFormat("f4", 1, 4),
    "f8": BufferFormat("f8", 1, 8),
    # Unsigned Integers
    "u": BufferFormat("u", 1, 4),
    "u1": BufferFormat("u1", 1, 1),
    "u2": BufferFormat("u2", 1, 2),
    "u4": BufferFormat("u4", 1, 4),
    # Signed Integer
    "i": BufferFormat("i", 1, 4),
    "i1": BufferFormat("i1", 1, 1),
    "i2": BufferFormat("i2", 1, 2),
    "i4": BufferFormat("i4", 1, 4),
    # Normalized float
    "nf": BufferFormat("nf", 1, 4),
    "nf1": BufferFormat("nf1", 1, 1),
    "nf2": BufferFormat("nf2", 1, 2),
    "nf4": BufferFormat("nf4", 1, 4),
    # Normalized uint
    "nu": BufferFormat("nu", 1, 4),
    "nu1": BufferFormat("nu1", 1, 1),
    "nu2": BufferFormat("nu2", 1, 2),
    "nu4": BufferFormat("nu4", 1, 4),
    # Normalized int
    "ni": BufferFormat("ni", 1, 4),
    "ni1": BufferFormat("ni1", 1, 1),
    "ni2": BufferFormat("ni2", 1, 2),
    "ni4": BufferFormat("ni4", 1, 4),
}
