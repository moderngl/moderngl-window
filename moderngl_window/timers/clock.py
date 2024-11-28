import time
from typing import Any, Optional

from moderngl_window.timers.base import BaseTimer


class Timer(BaseTimer):
    """Timer based on python ``time``."""

    def __init__(self, **kwargs: Any) -> None:
        self._start_time: Optional[float] = None
        self._stop_time: Optional[float] = None
        self._pause_time: Optional[float] = None
        self._last_frame = 0.0
        self._offset = 0.0

    @property
    def is_paused(self) -> bool:
        """bool: The pause state of the timer"""
        return self._pause_time is not None

    @property
    def is_running(self) -> bool:
        """bool: Is the timer currently running?"""
        return self._pause_time is None

    @property
    def time(self) -> float:
        """Get or set the current time.
        This can be used to jump around in the timeline.

        Returns:
            The current time in seconds
        """
        if self._start_time is None:
            return 0.0

        if self.is_paused and self._pause_time is not None:
            return self._pause_time - self._offset - self._start_time

        return time.time() - self._start_time - self._offset

    @time.setter
    def time(self, value: float) -> None:
        if value < 0:
            value = 0.0

        self._offset += self.time - value

    def next_frame(self) -> tuple[float, float]:
        """
        Get the time and frametime for the next frame.
        This should only be called once per frame.

        Returns:
            tuple[float, float]: current time and frametime
        """
        current = self.time
        delta, self._last_frame = current - self._last_frame, current
        return current, delta

    def start(self) -> None:
        """Start the timer by recoding the current ``time.time()``
        preparing to report the number of seconds since this timestamp.
        """
        if self._start_time is None:
            self._start_time = time.time()
            self._last_frame = 0.0
        elif self._pause_time is not None:
            self._offset += time.time() - self._pause_time
            self._pause_time = None
        else:
            print("The timer is already started")

    def pause(self) -> None:
        """Pause the timer by setting the internal pause time using ``time.time()``"""
        self._pause_time = time.time()

    def toggle_pause(self) -> None:
        """Toggle the paused state"""
        if self.is_paused:
            self.start()
        else:
            self.pause()

    def stop(self) -> tuple[float, float]:
        """
        Stop the timer. Should only be called once when stopping the timer.

        Returns:
            tuple[float, float]: Current position in the timer, actual running duration
        """
        if self._start_time is None:
            return 0.0, 0.0

        self._stop_time = time.time()
        return (
            self._stop_time - self._start_time - self._offset,
            self._stop_time - self._start_time,
        )
