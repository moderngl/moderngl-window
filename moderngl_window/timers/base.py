from typing import Tuple


class BaseTimer:
    """
    A timer controls the time passed into the the render function.
    This can be used in creative ways to control the current time
    such as basing it on current location in an audio file.

    A core feature of a timer is being able to:

    * Pause the current

    All methods must be implemented.
    """

    @property
    def is_paused(self) -> bool:
        """The pause state of the timer"""
        raise NotImplementedError()

    @property
    def is_running(self) -> bool:
        """Is the timer currently running?"""
        raise NotImplementedError()

    @property
    def time(self) -> float:
        """
        Get the current time in seconds

        Returns:
            The current time in seconds
        """
        raise NotImplementedError()

    @time.setter
    def time(self, value: float):
        """
        Set the current time in seconds.

        Args:
            value (float): The new time
        """
        raise NotImplementedError()

    def next_frame(self) -> Tuple[float, float]:
        """
        Get the time and frametime for the next frame
        """
        raise NotImplementedError()

    def start(self):
        """
        Start the timer initially or resume after pause
        Raises:
            NotImplementedError
        """
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
            (float, float) Current position in the timer, actual running duration
        """
        raise NotImplementedError()
