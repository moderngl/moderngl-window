import moderngl_window as mglw
from moderngl_window.conf import settings


def main():
    settings.WINDOW['class'] = 'moderngl_window.context.headless.Window'
    window = mglw.create_window_from_settings()

    frames = 0
    while not window.is_closing:
        window.use()
        window.clear()
        # Render stuff here
        window.swap_buffers()

        frames += 1
        if frames > 10:
            break

    window.destroy()


if __name__ == '__main__':
    main()
