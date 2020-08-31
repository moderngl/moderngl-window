import sched
import time
from moderngl_window.timers.base import BaseTimer


class Scheduler:
    def __init__(self, timer=time.time):
        if isinstance(timer, BaseTimer):
            # the timer might not be started, so check before getting the time
            timefunc = lambda: timer.time if timer._start_time else 0
        elif callable(timer):
            timefunc = timer
        else:
            raise ValueError(
                "timer, {}, has to be a instance of BaseTimer or a callable!".format(
                    timer
                )
            )

        self._events = dict()
        self._event_id = 0

        self._scheduler = sched.scheduler(timefunc, time.sleep)

    def run_once(self, action, delay, *, priority=1, argument=(), kwargs=dict()) -> int:
        """Schedule a function for execution after a delay.

        :param action: function to be called
        :type action: callable
        :param delay: delay in seconds
        :type delay: float
        :param priority: priority for this event, lower is more important, defaults to 1
        :type priority: int, optional
        :param argument: arguments for the action, defaults to ()
        :type argument: tuple, optional
        :param kwargs: keyword arguments for the action, defaults to dict()
        :type kwargs: dict, optional
        :return: returns a event id that can be canceled
        :rtype: int
        """
        event = self._scheduler.enter(delay, priority, action, argument, kwargs)
        self._events[self._event_id] = event
        self._event_id += 1
        return self._event_id - 1

    def run_at(self, action, time, *, priority=1, argument=(), kwargs=dict()) -> int:
        """Schedule a function to be executed at a certain time.

        :param action: function to be called
        :type action: callable
        :param time: epochtime in seconds
        :type time: float
        :param priority: priority for this event, lower is more important, defaults to 1
        :type priority: int, optional
        :param argument: arguments for the action, defaults to ()
        :type argument: tuple, optional
        :param kwargs: keyword arguments for the action, defaults to dict()
        :type kwargs: dict, optional
        :return: returns a event id that can be canceled
        :rtype: int
        """
        event = self._scheduler.enterabs(time, priority, action, argument, kwargs)
        self._events[self._event_id] = event
        self._event_id += 1
        return self._event_id - 1

    def run_every(
        self, action, delay, *, priority=1, initial_delay=0, argument=(), kwargs=dict()
    ) -> int:
        """Schedule a recurring function to be called every `delay` seconds after a initial delay.

        :param action: function to be called
        :type action: callable
        :param delay: delay in seconds
        :type delay: float
        :param priority: priority for this event, lower is more important, defaults to 1
        :type priority: int, optional
        :param argument: arguments for the action, defaults to ()
        :type argument: tuple, optional
        :param kwargs: keyword arguments for the action, defaults to dict()
        :type kwargs: dict, optional
        :return: returns a event id that can be canceled
        :rtype: int
        """
        recurring_event = self._recurring_event_factory(
            action, argument, kwargs, (delay, priority), self._event_id
        )
        event = self._scheduler.enter(initial_delay, priority, recurring_event)
        self._events[self._event_id] = event
        self._event_id += 1
        return self._event_id - 1

    def _recurring_event_factory(
        self, function, arguments, kwargs, scheduling_info, id
    ):
        """factory for creating recurring events that will reschedule themselves.

        :param function: function to be called
        :type function: callable
        :param arguments: arguments for the function
        :type arguments: tuple
        :param kwargs: keyword arguments for the function
        :type kwargs: dict
        :param scheduling_info: tuple of information for scheduling the event
        :type scheduling_info: tuple
        :param id: the id the event will get
        :type id: int
        :return: returns a callable that will reschedule itself
        :rtype: callable
        """

        def _f():
            function(*arguments, **kwargs)
            event = self._scheduler.enter(*scheduling_info, _f)
            self._events[id] = event

        return _f

    def execute(self) -> None:
        """runs the scheduler without blocking and executes any expired events.
        """
        self._scheduler.run(blocking=False)

    def cancel(self, event_id: int, delay: float = 0) -> None:
        """cancel a scheduled event.

        :param event_id: the event_id to be canceled
        :type event_id: int
        :param delay: a delay before canceling a event
        :type delay: float
        :raises ValueError: when the event can't be found
        """
        if delay == 0:
            self._cancel(event_id)
        else:
            self.run_once(self._cancel, delay, priority=0, argument=(event_id,))

    def _cancel(self, event_id: int):
        if event_id not in self._events:
            raise ValueError(
                "Recurring event with id {} does not exist".format(event_id)
            )
        event = self._events.pop(event_id)
        self._scheduler.cancel(event)
