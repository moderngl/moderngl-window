import datetime
import os
from typing import Any, Optional, Union

import moderngl

from moderngl_window.timers.clock import Timer


class BaseVideoCapture:
    """
    ``BaseVideoCapture`` is a base class to video capture

    Args:
        source (moderngl.Texture, moderngl.Framebuffer): the source of the capture
        framerate (int, float) : the framerate of the video, by thefault is 60 fps

    if the source is texture there are some requirements:
        - dtype = 'f1';
        - components >= 3.
    """

    def __init__(
        self,
        source: Union[moderngl.Texture, moderngl.Framebuffer],
        framerate: Union[int, float] = 60,
    ):

        self._source = source
        self._framerate = framerate

        self._recording: Optional[bool] = False

        self._last_time: float = 0.0
        self._filename: str = ""
        self._width: Optional[int] = None
        self._height: Optional[int] = None

        self._timer = Timer()

        self._components: int = 0  # for textures

        if isinstance(self._source, moderngl.Texture):
            self._components = self._source.components

    def _dump_frame(self, frame: Any) -> None:
        """
        custom function called during self.save()

        Args:
            frame: frame data in bytes
        """
        raise NotImplementedError("override this function")

    def _start_func(self) -> bool:
        """
        custom function called during self.start_capture()

        must return a True if this function complete without errors
        """
        raise NotImplementedError("override this function")

    def _release_func(self) -> None:
        """
        custom function called during self.release()
        """
        raise NotImplementedError("override this function")

    def _get_wh(self) -> tuple[int, int]:
        """
        Return a tuple of the width and the height of the source
        """
        return self._source.width, self._source.height

    def _remove_file(self) -> None:
        """Remove the filename of the video is it exist"""
        if os.path.exists(self._filename):
            os.remove(self._filename)

    def start_capture(
        self, filename: Optional[str] = None, framerate: Union[int, float] = 60
    ) -> None:
        """
        Start the capturing process

        Args:
            filename (str): name of the output file
            framerate (int, float): framerate of the video

        if filename is not specified it will be generated based
        on the datetime.
        """
        if self._recording:
            print("Capturing is already started")
            return

        # ensure the texture has the correct dtype and components
        if isinstance(self._source, moderngl.Texture):
            if self._source.dtype != "f1":
                print("source type: moderngl.Texture must be type `f1` ")
                return
            if self._components < 3:
                print("source type: moderngl.Texture must have at least 3 components")
                return

        if self._source is None:
            print("No source defined, there is nothing to record")
            return

        if not filename:
            now = datetime.datetime.now()
            filename = f"video_{now:%Y%m%d_%H%M%S}.mp4"

        self._filename = filename

        self._framerate = framerate
        self._width, self._height = self._get_wh()

        # if something goes wrong with the start
        # function, just stop and release the
        # capturing process
        if not self._start_func():
            self.release()
            print("Capturing failed")
            return

        self._timer.start()
        self._last_time = self._timer.time
        self._recording = True

    def save(self) -> None:
        """
        Save function to call at the end of render function
        """
        if not self._recording:
            return

        if self._source is None:
            return

        dt = 1.0 / self._framerate

        if self._timer.time - self._last_time > dt:

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

    def release(self) -> None:
        """
        Stop the recording process
        """
        if self._recording:
            self._release_func()

            self._timer.stop()
            print(f"Video file succesfully saved as {self._filename}")
        self._recording = None
