import sched
import time


class Scheduler:
    def __init__(self, timefunc=None):
        if timefunc is None:
            # try getting the timer for our window or use time.time
            pass
        else:
            timefunc = time.time

        self._recurring_events = dict()
        self._recurring_event_id = 0

        self._scheduler = sched.scheduler(timefunc, time.sleep)

    def run_once(self, action, delay, priority=1, argument=(), kwargs=dict()):
        return self._scheduler.enter(delay, priority, action, argument, kwargs)

    def run_at(self, action, time, priority=1, argument=(), kwargs=dict()):
        return self._scheduler.enterabs(time, priority, action, argument, kwargs)

    def run_every(self, action, delay, priority=1, argument=(), kwargs=dict()):
        recurring_event = self.recurring_event_factory(
            action, argument, kwargs, (delay, priority), self._recurring_event_id
        )

        event = self.run_once(recurring_event, delay, priority)
        self._recurring_events[self._recurring_event_id] = event
        self._recurring_event_id += 1
        return self._recurring_event_id - 1

    def recurring_event_factory(self, function, arguments, kwargs, scheduling_info, id):
        def _f():
            function(*arguments, **kwargs)
            event = self.run_once(_f, *scheduling_info)
            self._recurring_events[id] = event

        return _f

    def execute(self):
        self._scheduler.run(blocking=False)

    def cancel(self, event):
        if type(event) is not sched.Event:
            if event not in self._recurring_events:
                raise ValueError(
                    "Recurring event with id {} does not exist".format(event)
                )
            event = self._recurring_events.pop(event)
        self._scheduler.cancel(event)
