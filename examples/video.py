from typing import Tuple
from pathlib import Path

import moderngl_window
from moderngl_window import geometry
import av


class Decoder:

    def __init__(self, path: str):
        self.container = av.open(path)
        self.video = self.container.streams[0]
        self.video.thread_type = 'AUTO'

    @property
    def duration(self) -> float:
        """float: Number of frames in the video"""
        return self.video.duration * self.video.time_base.numerator / self.video.time_base.denominator

    @property
    def end_time(self):
        return self.video.end_time

    @property
    def average_rate(self) -> float:
        """The average framerate as a float"""
        rate = self.video.average_rate
        return rate.numerator / rate.denominator

    @property
    def frames(self) -> int:
        """int: Number of frames in the video"""
        return self.video.frames

    @property
    def video_size(self) -> Tuple[int, int]:
        """Tuple[int, int]: The width and height of the video in pixels"""
        return self.video.width, self.video.height

    def seek(self):
        pass

    def gen_frames(self):
        for packet in self.container.demux(video=0):
            for frame in packet.decode():
                yield frame.to_rgb().planes[0]

class VideoTest(moderngl_window.WindowConfig):
    gl_version = (3, 3)
    title = "Video Player"
    resource_dir = Path(__file__).parent.resolve() / 'resources'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.decoder = Decoder("C:\\Users\\efors\\Videos\\No Man's Sky\\No Man's Sky 2020.01.30 - 08.37.59.01.mp4")
        print('size', self.decoder.video_size)
        print('frames', self.decoder.frames)
        print('duration', self.decoder.duration)
        print('average_rate', self.decoder.average_rate)

        self.quad = geometry.quad_fs()
        self.program = self.load_program('programs/texture_flipped.glsl')
        self.texture = self.ctx.texture(self.decoder.video_size, 3)

        self.frames = self.decoder.gen_frames()

    def render(self, time, frametime):
        data = next(self.frames)
        self.texture.write(data)
        self.texture.use(0)
        self.quad.render(self.program)


if __name__ == '__main__':
    VideoTest.run()
