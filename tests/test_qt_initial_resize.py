from importlib import import_module
from unittest.mock import Mock

import pytest

from moderngl_window.context.base import BaseWindow


@pytest.fixture(params=["pyqt5", "pyside2"])
def qt_window(request, monkeypatch):
    pytest.importorskip({"pyqt5": "PyQt5", "pyside2": "PySide2"}[request.param])
    module = import_module(f"moderngl_window.context.{request.param}.window")
    app = module.QtWidgets.QApplication.instance()
    if app is None:
        monkeypatch.setenv("QT_QPA_PLATFORM", "offscreen")
        app = module.QtWidgets.QApplication([])
    window = module.Window.__new__(module.Window)
    BaseWindow.__init__(window)
    window._widget = module.QtWidgets.QWidget()
    window.set_default_viewport = Mock()
    window.resize_func = Mock()
    yield window
    window._widget.close()


def test_resize_before_context_creation(qt_window):
    assert not hasattr(qt_window, "_ctx")
    qt_window.resize(640, 480)
    ratio = qt_window._widget.devicePixelRatio()
    assert qt_window.size == (640 // ratio, 480 // ratio)
    assert qt_window.buffer_size == (640, 480)
    qt_window.set_default_viewport.assert_not_called()
    qt_window.resize_func.assert_called_once_with(640, 480)


def test_resize_after_context_creation(qt_window):
    qt_window._ctx = object()
    qt_window.resize(800, 600)
    assert qt_window.buffer_size == (800, 600)
    qt_window.set_default_viewport.assert_called_once_with()
    qt_window.resize_func.assert_called_once_with(800, 600)
