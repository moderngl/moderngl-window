import time
from unittest import TestCase

from moderngl_window.timers import clock


class TimerTestCase(TestCase):

    def test_clock_timer(self):
        """Quick and dirty clock timer test"""
        timer = clock.Timer()
        timer.start()
        time.sleep(0.1)
        self.assertFalse(timer.is_paused)
        self.assertTrue(timer.time > 0)
        timer.pause()
        self.assertTrue(timer.is_paused)
        timer.toggle_pause()
        self.assertFalse(timer.is_paused)
        self.assertTrue(timer.is_running)
        timer.time = 10.0
        timer.next_frame()
        pos, duration = timer.stop()
        self.assertTrue(pos >= 10)
        self.assertTrue(duration >= 0)

    def test_not_started(self) -> None:
        """Make sure the timer return 0 when it is never started"""
        timer = clock.Timer()
        t, real_t = timer.stop()
        self.assertTrue(t == 0)
        self.assertTrue(real_t == 0)
