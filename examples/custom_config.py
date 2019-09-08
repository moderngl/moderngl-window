import moderngl_window
from moderngl_window.conf import settings


def main():
    # settings.WINDOW['class'] = 'moderngl_window.context.headless.Window'
    window = moderngl_window.create_window_from_settings()

    while not window.is_closing:
        window.use()
        window.clear()
        # Render stuff here
        window.swap_buffers()

    window.destroy()


if __name__ == '__main__':
    main()
