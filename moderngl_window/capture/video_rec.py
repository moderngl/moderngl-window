# import logging
import subprocess
import datetime

import moderngl
from moderngl_window.timers.clock import Timer


class VideoCapture:
    """
        ``VideoCapture`` it's an utility class to capture runtime render
        and save it as video. 
        
        Example:

        .. code:: python

            import moderngl_window
            from moderngl_window.capture import VideoCapture

            class CaptureTest(modenrgl_window.WindowConfig):
                
                def __init__(self, **kwargs):
                    super().__init__(**kwargs)
                    # do other initialization 

                    # define VideoCapture class
                    self.cap = VideoCapture()

                    # start recording
                    self.cap.start_capture(
                        filename="video.mp4",
                        target_fb = self.wnd.fbo
                    )
                
                def render(self, time, frametime):
                    # do other render stuff

                    # call record function after
                    self.cap.dump()
                
                def close(self):
                    # if realease func is not called during 
                    # runtime. make sure to do it on the closing event
                    self.cap.release()


    """
    def __init__(self):

        self._ffmpeg = None
        self._video_timer = Timer()

        self._filename: str = None
        self._target_fb: moderngl.Framebuffer = None
        self._framerate: int = None

        self._last_frame = None
        self._recording = False
    
    @property
    def framerate(self) -> int:
        return self._framerate
    
    @framerate.setter
    def framerate(self, value: int):
        self._framerate = value
    
    @property
    def target_fb(self) -> moderngl.Framebuffer:
        return self._target_fb
    
    @target_fb.setter
    def target_fb(self, value: moderngl.Framebuffer):
        self._target_fb = value
    
    @property
    def filename(self) -> str:
        return self._filename
    
    @filename.setter
    def filename(self, value: str):
        self._filename = value
    

    def dump(self):
        """ Read data from the target framebuffer and dump the raw data 
            into ffmpeg stdin. 
            Call this function at the end of `render` function 
            
            Frame are saved respecting the video framerate.
        """
        if not self._recording:
            return
        
        # in theory to capture a frame at certain speed i'm testing if
        # the time passed after the last frame is at least dt = 1./target_fps .
        # This prevent the higher framerate during runtime to exceed the 
        # target framerate of the video. This doesn't work if runtime framerate 
        # is lower than target framerate.
        if  (self._video_timer.time - self._last_frame) >= 1./self._framerate:
            data = self._target_fb.read(components=3)
            self._ffmpeg.stdin.write(data)
            self._last_frame = self._video_timer.time


    def start(self, filename: str = None, target_fb: moderngl.Framebuffer = None, framerate=60):
        """
            Start ffmpeg pipe subprocess. 
            Call this at the end of __init__ function.

            Args:
                filename (str): name of the output file
                fb (moderngl.Framebuffer): target framebuffer to record
                framerate (int): framerate of the video

        """
        if not target_fb:
            raise Exception("target framebuffer can't be: None")
        else:
            self._target_fb = target_fb

        self._framerate = framerate
            
        if not filename:
            now = datetime.datetmie.now()
            filename = f'video_{now:%Y-%m-%d_%H:%M:%S.%f}.mp4'
        
        self._filename = filename
        
        width = target_fb.width
        height = target_fb.height

        # took from Wasaby2D project
        command = [
            'ffmpeg',
            '-y',  # (optional) overwrite output file if it exists
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', f'{width}x{height}',  # size of one frame
            '-pix_fmt', 'rgb24',
            '-r', f'{framerate}',  # frames per second
            '-i', '-',  # The imput comes from a pipe
            '-vf', 'vflip',
            '-an',  # Tells FFMPEG not to expect any audio
            filename,
        ]
        
        # ffmpeg binary need to be on the PATH.
        try:
            self._ffmpeg = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                bufsize=0
            )
        except FileNotFoundError:
            print("ffmpeg command not found.")
            return

        self._video_timer.start()
        self._last_frame = self._video_timer.time

        self._recording = True
        print("Started video Recording")

    def release(self):
        """
        Stop the recording process
        """
        if self._recording:
            self._ffmpeg.stdin.close()
            ret = self._ffmpeg.wait()
            if ret == 0:
                print("Video saved succesfully")
            else:
                print("Error writing video.")
            self._recording = None
            self._video_timer.stop()