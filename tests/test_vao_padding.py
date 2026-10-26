import struct

import moderngl
import numpy
import pytest

import moderngl_window as mglw
from moderngl_window.opengl import types
from moderngl_window.opengl.vao import VAO, VAOError


@pytest.mark.parametrize(
    "format_string,byte_size",
    [("x", 1), ("x1", 1), ("x2", 2), ("x4", 4), ("x8", 8), ("4x", 4)],
)
def test_padding_byte_size(format_string, byte_size):
    assert types.attribute_format(format_string).bytes_total == byte_size


@pytest.fixture(scope="module")
def ctx():
    context = moderngl.create_standalone_context(require=330)
    mglw.activate_context(ctx=context)
    yield context
    context.release()


def program(ctx, inputs, expression):
    return ctx.program(
        vertex_shader=(
            "#version 330\n"
            + "\n".join(f"in float {name};" for name in inputs)
            + f"\nout float result;\nvoid main() {{ result = {expression}; }}"
        ),
        varyings=["result"],
    )


@pytest.mark.parametrize(
    "format_string,leading,trailing",
    [("x 1f", 1, 0), ("1f 3x", 0, 3), ("1f 8x4", 0, 32), ("1x2 1f 1x8", 2, 8)],
)
def test_padded_vertex_values(ctx, format_string, leading, trailing):
    data = b"".join(bytes(leading) + struct.pack("f", v) + bytes(trailing) for v in (2, 5))
    shader = program(ctx, ["value"], "value")
    output = ctx.buffer(reserve=8)
    mesh = VAO(mode=moderngl.POINTS)
    try:
        mesh.buffer(data, format_string, ["value"])
        assert mesh.vertex_count == 2
        mesh.transform(shader, output, vertices=2)
        numpy.testing.assert_array_equal(numpy.frombuffer(output.read(), dtype="f4"), [2, 5])
    finally:
        mesh.release()
        output.release()
        shader.release()


@pytest.mark.parametrize(
    "inputs,expression,expected",
    [
        (["first"], "first", [2, 5]),
        (["second"], "second", [10, 20]),
        (["first", "second"], "first + second", [12, 25]),
    ],
)
def test_interleaved_padding_with_unused_attributes(ctx, inputs, expression, expected):
    data = struct.pack("f4xf4xf4xf4x", 2, 10, 5, 20)
    shader = program(ctx, inputs, expression)
    output = ctx.buffer(reserve=8)
    mesh = VAO(mode=moderngl.POINTS)
    try:
        mesh.buffer(data, "1f 1x4 1f 1x4", ["first", "second"])
        assert mesh.vertex_count == 2
        mesh.transform(shader, output, vertices=2)
        numpy.testing.assert_array_equal(numpy.frombuffer(output.read(), dtype="f4"), expected)
    finally:
        mesh.release()
        output.release()
        shader.release()


@pytest.mark.parametrize("suffix", ["/i", " /i", "/r", " /r", "/v", " /v"])
def test_padded_buffer_usage(ctx, suffix):
    shader = program(ctx, ["point", "offset"], "point + offset")
    output = ctx.buffer(reserve=16)
    mesh = VAO(mode=moderngl.POINTS)
    try:
        mesh.buffer(struct.pack("ff", 1, 2), "1f", ["point"])
        mesh.buffer(struct.pack("f4xf4x", 10, 20), "1f 1x4" + suffix, ["offset"])
        mesh.transform(shader, output, vertices=2, instances=2)
        expected = {"i": [11, 12, 21, 22], "r": [11, 12, 11, 12], "v": [11, 22, 11, 22]}
        numpy.testing.assert_array_equal(
            numpy.frombuffer(output.read(), dtype="f4"), expected[suffix[-1]]
        )
    finally:
        mesh.release()
        output.release()
        shader.release()


def test_padding_does_not_accept_an_attribute_name(ctx):
    mesh = VAO()
    buffer = ctx.buffer(reserve=8)
    try:
        with pytest.raises(VAOError, match="does not describe attributes"):
            mesh.buffer(buffer, "1f 1x4", ["value", "padding"])
    finally:
        mesh.release()
        buffer.release()
