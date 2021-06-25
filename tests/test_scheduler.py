import time
from unittest import TestCase
from moderngl_window.utils.scheduler import Scheduler
from moderngl_window.timers.clock import Timer


class SchedulingTestCase(TestCase):
    def set_value(self, v):
        self.test_value = v

    def increase_value(self):
        self.test_value += 1

    def test_clock_timer(self):
        """Quick and dirty scheduling test"""
        timer = Timer()
        timer.start()

        scheduler = Scheduler(timer)
        self.test_value = False
        scheduler.run_once(self.set_value, 0.1, arguments=(True,))
        time.sleep(0.11)
        scheduler.execute()
        self.assertTrue(self.test_value)

        self.test_value = 0
        event = scheduler.run_every(self.increase_value, 0.1)
        start = time.time()
        delta = time.time()
        while (delta - start) <= 0.5:
            # simulate a render loop
            print(self.test_value)
            time.sleep(0.01)
            scheduler.execute()
            delta = time.time()
        self.assertEqual(self.test_value, 5)
        # make sure it stays 5 once we cancel the event
        scheduler.cancel(event)
        time.sleep(0.11)
        scheduler.execute()
        self.assertEqual(self.test_value, 5)
