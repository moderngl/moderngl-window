import moderngl_window as mglw
from moderngl_window.conf import settings


def main():
    # settings.WINDOW['class'] = 'moderngl_window.context.headless.Window'
    window = mglw.create_window_from_settings()
    mglw.activate_context(window=window)

    while not window.is_closing:
        window.use()
        window.clear()
        # Render stuff here
        window.swap_buffers()

    window.destroy()


if __name__ == '__main__':
    main()
