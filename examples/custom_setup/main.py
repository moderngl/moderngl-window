import moderngl_window as mglw


def main():
    window = mglw.create_window_from_settings()

    while not window.is_closing:
        window.ctx.screen.use()
        window.ctx.screen.clear()
        # Render stuff here
        window.swap_buffers()


if __name__ == '__main__':
    main()
