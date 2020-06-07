"""
Example showing how we can modify the default cli argument parser.
"""
import math
from pathlib import Path

import moderngl_window


class ModifyParser(moderngl_window.WindowConfig):
    title = "Modify Parser"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        print('all arguments :', self.argv)
        # Print our custom argument
        print('message       :', self.argv.message)

    @classmethod
    def add_arguments(cls, parser):
        parser.add_argument('message', help="Some message")

    def render(self, time, frame_time):
        self.ctx.clear(
            (math.sin(time) + 1.0) / 2,
            (math.sin(time + 2) + 1.0) / 2,
            (math.sin(time + 3) + 1.0) / 2,
        )


if __name__ == '__main__':
    ModifyParser.run()
