import time

from moderngl_window.timers.base import BaseTimer


class Timer(BaseTimer):
    """
    Timer based on python ``time``.
    """
    def __init__(self, **kwargs):
        self._start_time = None
        self._stop_time = None
        self._pause_time = None
        self._offset = 0

    @property
    def is_paused(self) -> bool:
        """The pause state of the timer"""
        return self._pause_time is not None

    @property
    def is_running(self) -> bool:
        """Is the timer currently running?"""
        return self._pause_time is None

    @property
    def time(self) -> float:
        """
        Get the current time in seconds

        Returns:
            The current time in seconds
        """
        if self.is_paused:
            return self._pause_time - self._offset - self._start_time

        return time.time() - self._start_time - self._offset

    @time.setter
    def time(self, value: float):
        """
        Set the current time. This can be used to jump in the timeline.

        Args:
            value (float): The new time
        """
        if value < 0:
            value = 0

        self._offset += self.time - value

    def start(self):
        """
        Start the timer by recoding the current ``time.time()``
        preparing to report the number of seconds since this timestamp.
        """
        if self._start_time is None:
            self.start_time = time.time()
        else:
            self._offset += time.time() - self._pause_time
            self._pause_time = None

    def pause(self):
        """
        Pause the timer by setting the internal pause time using ``time.time()``
        """
        self._pause_time = time.time()

    def toggle_pause(self):
        """Toggle the paused state"""
        if self.is_paused:
            self.start()
        else:
            self.pause()

    def stop(self) -> float:
        """
        Stop the timer
        Returns:
            The time the timer was stopped
        """
        self._stop_time = time.time()
        return self._stop_time - self._start_time - self._offset
