from .base import BaseVideoCapture
import subprocess
import moderngl


class FFmpegCapture(BaseVideoCapture):
    """
        ``FFmpegCapture`` it's an utility class to capture runtime render
        and save it as video.

        Args:


        Example:

        .. code:: python

            import moderngl_window
            from moderngl_window.capture.ffmpeg import FFmpegCapture

            class CaptureTest(modenrgl_window.WindowConfig):

                def __init__(self, **kwargs):
                    super().__init__(**kwargs)
                    # do other initialization

                    # define VideoCapture class
                    self.cap = FFmpegCapture(source=self.wnd.fbo)

                    # start recording
                    self.cap.start_capture(
                        filename="video.mp4",
                        framerate=30
                    )

                def render(self, time, frametime):
                    # do other render stuff

                    # call record function after
                    self.cap.save()

                def close(self):
                    # if realease func is not called during
                    # runtime. make sure to do it on the closing event
                    self.cap.release()

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ffmpeg = None

    def _start_func(self) -> bool:
        """
            choose the right pixel format based on the number of components
            and start a ffmper pipe with a subprocess.
        """
        pix_fmt = 'rgb24'   # 3 component, 1 byte per color -> 24 bit

        # for the framebuffer is easier because i can read 3 component even if
        # the color attachment has less components
        if isinstance(self._source, moderngl.Texture) and self._components == 4:
            pix_fmt = 'rgba'  # 4 component , 1 byte per color -> 32 bit

        command = [
            'ffmpeg',
            '-hide_banner',
            '-loglevel', 'error', '-stats',  # less verbose, only stats of recording
            '-y',  # (optional) overwrite output file if it exists
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', f'{self._width}x{self._height}',  # size of one frame
            '-pix_fmt', pix_fmt,
            '-r', f'{self._framerate}',  # frames per second
            '-i', '-',  # The imput comes from a pipe
            '-vf', 'vflip',
            '-an',  # Tells FFMPEG not to expect any audio
            self._filename,
        ]

        # ffmpeg binary need to be on the PATH.
        try:
            self._ffmpeg = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                bufsize=0
            )
        except FileNotFoundError:
            print("ffmpeg command not found. Be sure to add it to PATH")
            return

        return True

    def _release_func(self):
        """
        Safely release the capture
        """
        self._ffmpeg.stdin.close()
        _ = self._ffmpeg.wait()

    def _dump_frame(self, frame):
        """
        write the frame data in to the ffmpeg pipe
        """
        self._ffmpeg.stdin.write(frame)
