import sched
import time
from moderngl_window.timers.base import BaseTimer


class Scheduler:
    def __init__(self, timer: BaseTimer):
        """Create a Scheduler object to handle events.

        Args:
            timer (BaseTimer): timer to use, subclass of BaseTimer.

        Raises:
            ValueError: timer is not a valid argument.
        """
        if not isinstance(timer, BaseTimer):
            raise ValueError(
                "timer, {}, has to be a instance of BaseTimer or a callable!".format(
                    timer
                )
            )

        self._events = dict()
        self._event_id = 0

        self._scheduler = sched.scheduler(lambda: timer.time, time.sleep)

    def run_once(
        self, action, delay: float, *, priority: int = 1, arguments=(), kwargs=dict()
    ) -> int:
        """Schedule a function for execution after a delay.

        Args:
            action (callable): function to be called.
            delay (float): delay in seconds.
            priority (int, optional): priority for this event, lower is more important. Defaults to 1.
            arguments (tuple, optional): arguments for the action. Defaults to ().
            kwargs (dict, optional): keyword arguments for the action. Defaults to dict().

        Returns:
            int: event id that can be canceled.
        """
        event = self._scheduler.enter(delay, priority, action, arguments, kwargs)
        self._events[self._event_id] = event
        self._event_id += 1
        return self._event_id - 1

    def run_at(
        self, action, time: float, *, priority: int = 1, arguments=(), kwargs=dict()
    ) -> int:
        """Schedule a function to be executed at a certain time.

        Args:
            action (callable): function to be called.
            time (float): epoch time at which the function should be called.
            priority (int, optional): priority for this event, lower is more important. Defaults to 1.
            arguments (tuple, optional): arguments for the action. Defaults to ().
            kwargs (dict, optional): keyword arguments for the action. Defaults to dict().

        Returns:
            int: event id that can be canceled.
        """
        event = self._scheduler.enterabs(time, priority, action, arguments, kwargs)
        self._events[self._event_id] = event
        self._event_id += 1
        return self._event_id - 1

    def run_every(
        self,
        action,
        delay: float,
        *,
        priority: int = 1,
        initial_delay: float = 0.0,
        arguments=(),
        kwargs=dict()
    ) -> int:
        """Schedule a recurring function to be called every `delay` seconds after a initial delay.

        Args:
            action (callable): function to be called.
            delay (float): delay in seconds.
            priority (int, optional): priority for this event, lower is more important. Defaults to 1.
            initial_delay (float, optional): initial delay in seconds before executing for the first time.
            Defaults to 0. arguments (tuple, optional): arguments for the action. Defaults to ().
            kwargs (dict, optional): keyword arguments for the action. Defaults to dict().

        Returns:
            int: event id that can be canceled.
        """
        recurring_event = self._recurring_event_factory(
            action, arguments, kwargs, (delay, priority), self._event_id
        )
        event = self._scheduler.enter(initial_delay, priority, recurring_event)
        self._events[self._event_id] = event
        self._event_id += 1
        return self._event_id - 1

    def _recurring_event_factory(
        self, function, arguments, kwargs, scheduling_info, id
    ):
        """Factory for creating recurring events that will reschedule themselves.

        Args:
            function (callable): function to be called.
            arguments (tuple): arguments for the function.
            kwargs (dict): keyword arguments for the function.
            scheduling_info (tuple): tuple of information for scheduling the task.
            id (int): event id this event should be assigned to.
        """

        def _f():
            function(*arguments, **kwargs)
            event = self._scheduler.enter(*scheduling_info, _f)
            self._events[id] = event

        return _f

    def execute(self) -> None:
        """Run the scheduler without blocking and execute any expired events.
        """
        self._scheduler.run(blocking=False)

    def cancel(self, event_id: int, delay: float = 0) -> None:
        """Cancel a previously scheduled event.

        Args:
            event_id (int): event to be canceled
            delay (float, optional): delay before canceling the event. Defaults to 0.
        """
        if delay == 0:
            self._cancel(event_id)
        else:
            self.run_once(self._cancel, delay, priority=0, arguments=(event_id,))

    def _cancel(self, event_id: int):
        if event_id not in self._events:
            raise ValueError(
                "Recurring event with id {} does not exist".format(event_id)
            )
        event = self._events.pop(event_id)
        self._scheduler.cancel(event)
