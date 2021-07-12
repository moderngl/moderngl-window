from .base import BaseVideoCapture
import subprocess

class FFmpegCapture(BaseVideoCapture):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._ffmpeg = None
    
    def _start_func(self):

        # took from Wasaby2D project
        command = [
            'ffmpeg',
            '-hide_banner',
            '-loglevel', 'error', '-stats', # less verbose, only stats of recording
            '-y',  # (optional) overwrite output file if it exists
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', f'{self._width}x{self._height}',  # size of one frame
            '-pix_fmt', 'rgb24',
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
    
    def _release_func(self):
        self._ffmpeg.stdin.close()
        ret = self._ffmpeg.wait()
    
    def _dump_frame(self, frame):
        self._ffmpeg.stdin.write(frame)
