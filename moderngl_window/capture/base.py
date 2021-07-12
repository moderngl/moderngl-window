import logging
from typing import Union

import datetime
import moderngl
from moderngl_window.timers.clock import Timer

class BaseVideoCapture:
    
    def __init__(
        self,
        source: Union[moderngl.Texture, moderngl.Framebuffer] = None,
        framerate: Union[int, float] = 60,
    ):

        self._source = source
        self._framerate = framerate

        self._recording = False

        self._last_time : float = None
        self._filename : str = None
        self._width: int = None
        self._height: int = None

        self._timer = Timer()


    def _dump_frame(self, frame):
        raise NotImplementedError("override this function")
    
    def _start_func(self,):
        raise NotImplementedError("override this function")

    def _release_func(self):
        raise NotImplementedError("override this function")

    def save(self):
        
        if not self._recording:
            return

        frame = None
        dt = 1./self._framerate

        if self._timer.time-self._last_time > dt:
            # print("frame")
            self._last_time = self._timer.time

            if isinstance(self._source, moderngl.Framebuffer):
                # get data from framebuffer
                frame = self._source.read(components=3)
                self._dump_frame(frame)  # override this function
            else:
                # get data from texture
                raise NotImplementedError("can't retreive data from type: moderngl.Texture yet...")

    def _get_wh(self):
        if isinstance(self._source, moderngl.Framebuffer):
            return self._source.width, self._source.height
        else:
            raise NotImplementedError("can't get width and height from type: moderngl.Texture yet...")

    def start_capture(self, filename: str = None, framerate: Union[int, float] = 60):
        
        if self._recording:
            logging.warn("Capturing is already started")
            return

        if not filename:
            now = datetime.datetime.now()
            filename = f'video_{now:%Y%m%d_%H%M%S}.mp4'
        
        self._filename = filename

        self._framerate = framerate
        self._width, self._height = self._get_wh()

        self._start_func() # override this function

        self._timer.start()
        self._last_time = self._timer.time
        self._recording = True
    
    def release(self):
        self._release_func() # override this function

        self._timer.stop()
        self._recording = None
        logging.info(f"Video file succesfully saved as {self._filename}")

