"""
Video player implementation using PyAV for decoding and ModernGL for rendering.
Requires: pip install av
"""

import logging
from pathlib import Path
from typing import Union, Literal

import av
import moderngl
import moderngl_window
from moderngl_window import geometry

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class VideoDecoder:
    """Handles video decoding using PyAV."""

    def __init__(self, path: Union[str, Path]):
        self._path = Path(path)
        if not self._path.exists():
            raise FileNotFoundError(f"Video file not found: {self._path}")

        self.container = av.open(str(self._path))
        self.video = self.container.streams.video[0]
        self.video.thread_type = "AUTO"
        self.video.codec_context.pix_fmt = "yuv420p"

        self._current_frame = 0

    @property
    def duration(self) -> float:
        """Video duration in seconds."""
        if self.video.duration is None:
            return float(self.container.duration * float(self.container.time_base))
        return float(self.video.duration * float(self.video.time_base))

    @property
    def framerate(self) -> float:
        """Average framerate."""
        rate = self.video.average_rate
        return rate.numerator / rate.denominator

    @property
    def size(self) -> tuple[int, int]:
        """Video dimensions (width, height)."""
        return self.video.width, self.video.height

    def seek(self, time_seconds: float) -> None:
        """Seek to specified time position."""
        try:
            time_seconds = max(0, min(time_seconds, self.duration))
            timestamp = int(time_seconds / float(self.video.time_base))
            self.container.seek(timestamp, stream=self.video)
            self._current_frame = int(time_seconds * self.framerate)
            self.container.decode(video=0)
        except Exception as e:
            logger.error(f"Seek failed: {e}")
            self.container.seek(0)
            self._current_frame = 0

    def get_frames(self):
        """Generate video frames from current position."""
        try:
            for packet in self.container.demux(video=0):
                for frame in packet.decode():
                    self._current_frame += 1
                    yield frame.to_rgb().planes[0]
        except Exception as e:
            logger.error(f"Frame generation error: {e}")

    @property
    def frames(self) -> int:
        """Total number of frames in video."""
        return int(self.duration * self.framerate)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.container.close()

    def close(self):
        """Explicitly close the video container."""
        self.container.close()


class VideoPlayer:
    """Handles video playback and rendering using ModernGL."""

    # Add constants at class level
    FRAME_DIFF_THRESHOLD = 5
    MAX_BEHIND_COUNT = 10
    SKIP_OFFSET = 2

    def __init__(self, ctx: moderngl.Context, path: Union[str, Path]):
        self._ctx = ctx
        self._decoder = VideoDecoder(path)
        self._texture = self._ctx.texture(self._decoder.size, 3, dtype="f1")
        self._frames = self._decoder.get_frames()

        self._current_frame = 0
        self._target_frame = 0
        self._behind_count = 0
        self._paused = False

    @property
    def fps(self) -> float:
        return self._decoder.framerate

    @property
    def duration(self) -> float:
        return self._decoder.duration

    @property
    def frames(self) -> int:
        return self._decoder.frames

    @property
    def size(self) -> tuple[int, int]:
        return self._decoder.size

    @property
    def texture(self) -> moderngl.Texture:
        return self._texture

    def update(self, time: float) -> bool:
        """Update video playback state."""
        if self._paused:
            return False

        self._target_frame = int(time * self.fps)
        frame_diff = self._target_frame - self._current_frame

        # Check if we've reached the end
        if self._current_frame >= self.frames:
            self.seek(0)
            return True

        # Handle falling behind
        if frame_diff > self.FRAME_DIFF_THRESHOLD:
            self._behind_count += 1
            skip_to = min(self._target_frame - self.SKIP_OFFSET, self.frames - 1)

            if self._behind_count > self.MAX_BEHIND_COUNT:
                self._decoder.seek(skip_to / self.fps)
                self._frames = self._decoder.get_frames()
                self._current_frame = skip_to
                self._behind_count = 0
            else:
                try:
                    while self._current_frame < skip_to:
                        next(self._frames)
                        self._current_frame += 1
                except StopIteration:
                    self.seek(0)
                    return True
        else:
            self._behind_count = max(0, self._behind_count - 1)
            if frame_diff > 0:
                try:
                    data = next(self._frames)
                    self._texture.write(data)
                    self._current_frame += 1
                except StopIteration:
                    self.seek(0)
                    return True

        return False

    def seek(self, time: float) -> None:
        """Seek to specified time position."""
        time = max(0, min(time, self.duration))
        self._decoder.seek(time)
        self._frames = self._decoder.get_frames()
        self._current_frame = int(time * self.fps)
        self._target_frame = self._current_frame
        self._behind_count = 0

    def toggle_pause(self) -> None:
        """Toggle pause state."""
        self._paused = not self._paused

    @property
    def current_frame(self) -> int:
        return self._current_frame

    @property
    def target_frame(self) -> int:
        return self._target_frame

    @property
    def is_paused(self) -> bool:
        return self._paused


class VideoPlayerWindow(moderngl_window.WindowConfig):
    """ModernGL window configuration for video playback."""

    gl_version = (3, 3)
    title = "Video Player"
    resource_dir = Path(__file__).parent.resolve() / "resources"
    vsync = True
    seek_time = 1.0  # Seconds to seek when using arrow keys
    log_level = logging.DEBUG

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize video player
        video_path = self.resource_dir / "videos" / "Lightning - 33049.mp4"

        self.player = VideoPlayer(self.ctx, video_path)

        # Setup rendering
        self.quad = geometry.quad_fs()
        self.program = self.load_program("programs/texture_flipped.glsl")

        # Setup stats printing
        self._last_print_time = 0

    def on_render(self, time: float, frametime: float) -> None:
        """Render frame."""
        if self.player.update(time):  # Check if video ended
            self.timer.time = 0  # Reset timer if video ended

        # Render video
        self.player.texture.use(0)
        self.quad.render(self.program)

        # Print debug stats every 0.5 seconds regardless of pause state
        if (time - self._last_print_time) >= 0.5 or time < self._last_print_time:
            # Get FPS values with safety checks
            fps_avg = self.timer.fps_average if self.timer.time > 0 else 0.0

            logger.debug(
                "Movie Target FPS: %.1f | Window FPS: %.1f | Frame: %d/%d | \
                Time: %.2f/%.2f | Frame Diff: %d | Paused: %s",
                self.player.fps,
                fps_avg,
                self.player.current_frame,
                self.player.frames,
                self.timer.time,
                self.player.duration,
                self.player.target_frame - self.player.current_frame,
                self.player.is_paused,
            )
            self._last_print_time = time

    def _handle_seek(self, direction: Literal["forward", "backward"]) -> None:
        """Handle seeking in video. direction: 'forward' or 'backward'"""
        seek_amount = self.seek_time if direction == "forward" else -self.seek_time
        new_time = max(0, min(self.player.duration, self.timer.time + seek_amount))

        if self.timer.is_paused:
            self.player.seek(new_time)
        else:
            self.timer.time = new_time
            self.player.seek(new_time)

    def on_key_event(self, key, action, modifiers) -> None:
        """Handle keyboard input."""
        super().on_key_event(key, action, modifiers)
        keys = self.wnd.keys

        if action == keys.ACTION_PRESS:
            if key == keys.LEFT:
                self._handle_seek("backward")
            elif key == keys.RIGHT:
                self._handle_seek("forward")
            elif key == keys.SPACE:
                self.timer.toggle_pause()
                self.player.toggle_pause()


if __name__ == "__main__":
    VideoPlayerWindow.run()
