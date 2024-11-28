from unittest import TestCase

import moderngl

import moderngl_window as mglw
from moderngl_window.conf import settings


class HeadlessTestCase(TestCase):
    """Test using a headless window/context"""
    window_size = (16, 16)
    aspect_ratio = 1.0
    gl_version = (4, 1)

    @classmethod
    def setUpClass(cls):
        """Create a headless window and activate the context"""
        settings.WINDOW['class'] = 'moderngl_window.context.headless.Window'
        settings.WINDOW['size'] = cls.window_size
        settings.WINDOW['aspect_ratio'] = cls.aspect_ratio
        settings.WINDOW['gl_version'] = cls.gl_version

        cls.window = mglw.create_window_from_settings()
        mglw.activate_context(window=cls.window)

    @property
    def ctx(self) -> moderngl.Context:
        """moderngl.Context: The active context"""
        return mglw.ctx()


class WindowConfigTestCase(TestCase):
    """Headless using windowconfig"""
    TestConfig = None
    config = None
    window = None

    @classmethod
    def setUpClass(cls):
        window_cls = mglw.get_local_window_cls('headless')
        cls.window = window_cls(
            title=cls.TestConfig.title,
            size=cls.TestConfig.window_size,
            resizable=cls.TestConfig.resizable,
            gl_version=cls.TestConfig.gl_version,
            aspect_ratio=cls.TestConfig.aspect_ratio,
            samples=cls.TestConfig.samples,
            cursor=cls.TestConfig.cursor,
        )
        cls.config = cls.TestConfig(
            wnd=cls.window,
            ctx=cls.window.ctx,
            timer=None,
        )
        cls.window.config = cls.config
        mglw.activate_context(window=cls.window)

    def ctx(self):
        return self.window.ctx
