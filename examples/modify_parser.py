"""
Example showing how we can modify the default cli argument parser.

Imagine we're making a small utility displaying a 3D object
from some file. We require a path to the file and and optional
argument if the model should be rendered as wireframe or not.
In addition we have an optional argument for changing the
window title.

Possible arguments should be:

python script.py path/to/file
python script.py path/to/file --wireframe
python script.py path/to/file --wireframe --title "Custom Window Title"
python script.py path/to/file --title "Custom Window Title"

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
        print('path      :', self.argv.path)
        print('wireframe :', self.argv.wireframe)
        print('title     :', self.argv.title)

        if self.argv.title:
            self.wnd.title = self.argv.title

    @classmethod
    def add_arguments(cls, parser):
        # Mandatory positional argument for the file to load
        parser.add_argument(
            'path',
            help="Path to the model to display",
        )
        # Optional flag for rendering the model in wireframe
        # This is simply enabled by adding "--wireframe" with no arguments
        parser.add_argument(
            '--wireframe',
            action="store_true",
            default=False,
            help="Display the model as a wireframe",
        )
        # Optional argument for window title
        parser.add_argument(
            '--title',
            type=str,
            help="Override the window title",
        )

    def render(self, time, frame_time):
        # Placeholder content
        self.ctx.clear(
            (math.sin(time) + 1.0) / 2,
            (math.sin(time + 2) + 1.0) / 2,
            (math.sin(time + 3) + 1.0) / 2,
        )


if __name__ == '__main__':
    ModifyParser.run()
