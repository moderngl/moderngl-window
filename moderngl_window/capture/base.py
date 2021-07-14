import os
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

        self._components: int = None

        if isinstance(self._source, moderngl.Texture):
            self._components = self._source.components


    def _dump_frame(self, frame):
        raise NotImplementedError("override this function")
    
    def _start_func(self) -> bool:
        raise NotImplementedError("override this function")

    def _release_func(self):
        raise NotImplementedError("override this function")

    def _get_wh(self):
        return self._source.width, self._source.height
    
    def _remove_file(self):
        if os.path.exists(self._filename):
            os.remove(self._filename)

    def start_capture(self, filename: str = None, framerate: Union[int, float] = 60):
        
        if self._recording:
            logging.info("Capturing is already started")
            return

        if isinstance(self._source, moderngl.Texture):
            if self._source.dtype != 'f1':
                logging.info("source type: moderngl.Texture must be type `f1` ")
                return
            if self._components < 3:
                logging.info("source type: moderngl.Texture must have at least 3 components")
                return 

        if not filename:
            now = datetime.datetime.now()
            filename = f'video_{now:%Y%m%d_%H%M%S}.mp4'
        
        self._filename = filename

        self._framerate = framerate
        self._width, self._height = self._get_wh()

        # if something goes wrong with the start
        # function, just stop and release the 
        # capturing process 
        if not self._start_func():
            self.release()
            logging.info("Capturing failed")
            return 

        self._timer.start()
        self._last_time = self._timer.time
        self._recording = True

    def save(self):
        
        if not self._recording:
            return

        dt = 1./self._framerate

        if self._timer.time-self._last_time > dt:
            
            # start counting
            self._last_time = self._timer.time

            if isinstance(self._source, moderngl.Framebuffer):
                # get data from framebuffer
                frame = self._source.read(components=3)
                self._dump_frame(frame)
            else:
                # get data from texture
                frame = self._source.read()
                self._dump_frame(frame)
     
    def release(self):
        if self._recording:
            self._release_func()

            self._timer.stop()
            self._recording = None
            logging.info(f"Video file succesfully saved as {self._filename}")
    

