import random

import moderngl_window
from moderngl_window.utils.scheduler import Scheduler


class CubeSimpleInstancedScheduler(moderngl_window.WindowConfig):
    """Schedule one-off and recurring events"""

    title = "Scheduling example"
    aspect_ratio = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # create a instance of the Scheduler and tell it to use the windows internal timer
        # if we dont pass a timer `time.time()` will be used.
        # by using the internal Timer class the pause and time setting functions
        # will effect our events aswell.
        self.scheduler = Scheduler(self.timer)

        # change the color every 1/2 seconds
        color_changing_event = self.scheduler.run_every(self.change_color, 1 / 2)
        # cancel the color changing event after 2 seconds using a priority of 2
        self.scheduler.cancel(color_changing_event, delay=2)
        # restart it after another 2 seconds (4 seconds total)
        color_changing_event = self.scheduler.run_every(
            self.change_color, 1 / 2, initial_delay=4
        )

        # after 5 seconds change the window title
        self.scheduler.run_once(self.change_title, 5, arguments=("Changed title",))

    def change_title(self, new_title):
        self.wnd.title = new_title

    def change_color(self):
        self.clear_color = (random.random(), random.random(), random.random(), 0)

    def render(self, time: float, frametime: float):
        self.scheduler.execute()


if __name__ == "__main__":
    moderngl_window.run_window_config(CubeSimpleInstancedScheduler)
