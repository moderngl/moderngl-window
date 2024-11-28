"""
Registry for rocket tracks
"""

from rocket.tracks import Track


class Tracks:
    """Registry for requested rocket tracks"""

    def __init__(self) -> None:
        self.tacks: list[Track] = []
        self.track_map: dict[str, Track] = {}

    def get(self, name: str) -> Track:
        """
        Get or create a Track object.

        :param name: Name of the track
        :return: Track object
        """
        name = name.lower()
        track = self.track_map.get(name)

        if not track:
            track = Track(name)
            self.tacks.append(track)
            self.track_map[name] = track

        return track


tracks = Tracks()
