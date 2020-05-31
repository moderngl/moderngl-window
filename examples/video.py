from typing import Tuple
from pathlib import Path

import moderngl
import moderngl_window
from moderngl_window import geometry
import av


class Decoder:

    def __init__(self, path: str):
        self.container = av.open(path)
        self.video = self.container.streams[0]
        self.video.thread_type = 'AUTO'
        self._last_packet = None
        time_base = self.video.time_base
        self._pos_step = int(time_base.denominator / time_base.numerator / self.average_rate)

    @property
    def duration(self) -> float:
        """float: Number of frames in the video"""
        if self.video.duration is None:
            return -1
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

    @property
    def current_pos(self):
        """The current position in the stream"""
        if self._last_packet:
            return self._last_packet.pts
        return 0

    @property
    def frame_step(self):
        """Position step for each frame"""
        return self._pos_step

    def time_to_pos(self, time: float) -> int:
        """Converts time to stream position"""
        time_base = self.video.time_base
        return int(time * time_base.denominator / time_base.numerator)

    def seek(self, position: int):
        """Seek to a position in the stream"""
        self.container.seek(position, stream=self.video)

    def gen_frames(self):
        for packet in self.container.demux(video=0):
            if packet.pts is not None:
                self._last_packet = packet
            for i, frame in enumerate(packet.decode()):
                yield frame.to_rgb().planes[0]


class Player:

    def __init__(self, ctx: moderngl.Context, path: str):
        self._ctx = ctx
        self._path = path
        self._decoder = Decoder(self._path)
        self._texture = self._ctx.texture(self._decoder.video_size, 3)
        self._frames = self._decoder.gen_frames()

        self._last_time = 0
        self._fps = self._decoder.average_rate

    @property
    def fps(self) -> float:
        """float: Framerate of the video"""
        return self._fps

    @property
    def duration(self) -> float:
        """float: Length of video in seconds"""
        return self._decoder.duration

    @property
    def frames(self) -> int:
        """int: The number of frames in the video"""
        return self._decoder.frames

    @property
    def video_size(self) -> Tuple[int, int]:
        """Tuple[int, int]: Video size in pixels"""
        return self._decoder.video_size

    @property
    def texture(self) -> moderngl.Texture:
        return self._texture

    def update(self, time: float):
        next_pos = self._decoder.time_to_pos(time)
        delta = next_pos - self._decoder.current_pos

        # Seek we are more than 3 frames off
        if abs(delta) > self._decoder.frame_step * 3:
            # print("SEEK", next_pos)
            self._decoder.seek(next_pos)
        else:
            if delta < self._decoder.frame_step:
                # print("SKIP")
                return

        # print((
        #     f"frame_step={self._decoder.frame_step}, "
        #     f"delta={delta}, "
        #     f"next_pos={next_pos}, "
        #     f"current_pos={self._decoder.current_pos}, "
        #     f"time={time}"
        # ))
        try:
            data = next(self._frames)
        except StopIteration:
            return
        self._texture.write(data)

    def next_frame(self) -> av.plane.Plane:
        """Get RGB data for the next frame.
        A VideoPlane is returned containing the RGB data.
        This objects supports the buffer protocol and can be written to a texture directly.
        """
        return next(self._frames)


class VideoTest(moderngl_window.WindowConfig):
    gl_version = (3, 3)
    title = "Video Player"
    resource_dir = Path(__file__).parent.resolve() / 'resources'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        path = "/Users/einarforselv/Downloads/test.avi"
        # path = "C:\\Users\\efors\\Videos\\No Man's Sky\\No Man's Sky 2020.01.30 - 08.37.59.01.mp4"
        # path = "C:\\Users\\efors\\Downloads\\DemoNoir.ivf"
        # path = "C:\\Users\\efors\\Videos\\Beat Saber\\Beat Saber 2020.04.04 - 02.40.22.05.mp4"
        self.player = Player(self.ctx, path)

        print("duration   :", self.player.duration)
        print("fps        :", self.player.fps)
        print("video_size :", self.player.video_size)
        print("frames     :", self.player.frames)
        print("step       :", self.player._decoder.frame_step)

        self.quad = geometry.quad_fs()
        self.program = self.load_program('programs/texture_flipped.glsl')

    def render(self, time, frametime):
        self.player.update(time)
        self.player.texture.use(0)
        self.quad.render(self.program)

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        # Key presses
        if action == keys.ACTION_PRESS:
            if key == keys.LEFT:
                self.timer.time = self.timer.time - 10

            if key == keys.RIGHT:
                self.timer.time = self.timer.time + 10

            if key == keys.SPACE:
                self.timer.toggle_pause()


if __name__ == '__main__':
    VideoTest.run()
