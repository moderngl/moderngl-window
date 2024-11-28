from typing import Any, Optional

from moderngl_window.meta.base import ResourceDescription


class DataDescription(ResourceDescription):
    """Describes data file to load.

    This is a generic resource description type
    for loading resources that are not textures, programs and scenes.
    That loaded class is used depends on the ``kind`` or the file extension.

    Currently used to load:

    - text files
    - json files
    - binary files

    .. code:: python

        # Describe a text file. Text loader is used based on file extension
        DataDescription(path='data/text.txt')

        # Describe a json file. Json loader is used based on file extension
        DataDescription(path='data/data.json')

        # Describe a binary file. Specify a binary loader should be used.
        DataDescription(path='data/data.bin', kind='binary')
    """

    default_kind: str = ""
    resource_type = "data"

    def __init__(
        self, path: Optional[str] = None, kind: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Initialize the resource description.

        Keyword Args:
            path (str): Relative path to the resource
            kind (str): The resource kind deciding loader class
            **kwargs: Additional custom attributes
        """
        kwargs.update({"path": path, "kind": kind})
        super().__init__(**kwargs)
