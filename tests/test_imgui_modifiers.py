from importlib import import_module
from types import SimpleNamespace

import pytest

from moderngl_window.context.base.keys import BaseKeys, KeyModifiers


@pytest.fixture(params=["classic", "bundle"])
def integration(request):
    if request.param == "classic":
        imgui = pytest.importorskip("imgui")
        module = import_module("moderngl_window.integrations.imgui")
    else:
        imgui = pytest.importorskip("imgui_bundle.imgui")
        module = import_module("moderngl_window.integrations.imgui_bundle")

    context = imgui.create_context()
    io = imgui.get_io()
    io.display_size = (16, 16)
    io.delta_time = 1 / 60
    # Test raw modifier input consistently instead of macOS Ctrl/Super swapping.
    io.config_mac_osx_behaviors = False
    if request.param == "bundle" and hasattr(imgui.BackendFlags_, "renderer_has_textures"):
        io.backend_flags |= imgui.BackendFlags_.renderer_has_textures
    else:
        io.fonts.get_tex_data_as_rgba32()

    renderer = module.ModernglWindowMixin()
    renderer.io = io
    renderer.wnd = SimpleNamespace(keys=BaseKeys)
    if request.param == "classic":
        renderer.REVERSE_KEY_MAP = {123: imgui.KEY_A}
    else:
        renderer.REVERSE_KEYMAP = {123: imgui.Key.a}

    def advance_frame():
        imgui.new_frame()
        imgui.end_frame()

    yield renderer, imgui, io, advance_frame, request.param
    imgui.destroy_context(context)


@pytest.mark.parametrize("mask", range(8))
def test_modifier_snapshot_updates_even_for_unmapped_keys(integration, mask):
    renderer, _, io, advance_frame, _ = integration
    modifiers = KeyModifiers()
    modifiers.shift = modifiers.ctrl = modifiers.alt = True
    renderer.key_event(999, BaseKeys.ACTION_PRESS, modifiers)
    advance_frame()
    assert (io.key_shift, io.key_ctrl, io.key_alt) == (True, True, True)

    modifiers.shift = bool(mask & 1)
    modifiers.ctrl = bool(mask & 2)
    modifiers.alt = bool(mask & 4)
    renderer.key_event(999, BaseKeys.ACTION_RELEASE, modifiers)
    advance_frame()
    assert (io.key_shift, io.key_ctrl, io.key_alt) == (
        modifiers.shift,
        modifiers.ctrl,
        modifiers.alt,
    )


def test_mapped_key_press_and_release_keep_modifier_state(integration):
    renderer, imgui, io, advance_frame, backend = integration
    modifiers = KeyModifiers()
    modifiers.ctrl = True
    renderer.key_event(123, BaseKeys.ACTION_PRESS, modifiers)
    advance_frame()
    assert io.key_ctrl
    down = io.keys_down[imgui.KEY_A] if backend == "classic" else imgui.is_key_down(imgui.Key.a)
    assert down

    renderer.key_event(123, BaseKeys.ACTION_RELEASE, modifiers)
    advance_frame()
    assert io.key_ctrl
    down = io.keys_down[imgui.KEY_A] if backend == "classic" else imgui.is_key_down(imgui.Key.a)
    assert not down
