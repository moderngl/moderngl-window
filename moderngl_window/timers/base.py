from typing import Tuple


class BaseTimer:
    """
    A timer controls the time passed into the the render function.
    This can be used in creative ways to control the current time
    such as basing it on current location in an audio file.

    All methods must be implemented.
    """

    @property
    def is_paused(self) -> bool:
        """bool: The pause state of the timer"""
        raise NotImplementedError()

    @property
    def is_running(self) -> bool:
        """bool: Is the timer currently running?"""
        raise NotImplementedError()

    @property
    def time(self) -> float:
        """Get or set the current time.
        This can be used to jump around in the timeline.

        Returns:
            float: The current time in seconds
        """
        raise NotImplementedError()

    @time.setter
    def time(self, value: float):
        raise NotImplementedError()

    def next_frame(self) -> Tuple[float, float]:
        """Get timer information for the next frame.

        Returns:
            Tuple[float, float]: The frametime and current time
        """
        raise NotImplementedError()

    def start(self):
        """Start the timer initially or resume after pause"""
        raise NotImplementedError()

    def pause(self):
        """Pause the timer"""
        raise NotImplementedError()

    def toggle_pause(self):
        """Toggle pause state"""
        raise NotImplementedError()

    def stop(self) -> Tuple[float, float]:
        """
        Stop the timer. Should only be called once when stopping the timer.

        Returns:
            Tuple[float, float]> Current position in the timer, actual running duration
        """
        raise NotImplementedError()
