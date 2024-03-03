# Standard Library
from pathlib import Path
from typing import Any

# Local
from misc_utils import export
from misc_utils.misc_utils import json_load, json_dump


@export
class JSONDict(dict):
    """A dictionary that can be serialized to and deserialized from a JSON file.

    Args:
    ----
        dict (dict): The dictionary to be serialized.

    Returns:
    -------
        JSONDict: The deserialized dictionary.
    """

    def __init__(self, path, *args, **kwargs):
        self.path = Path(path)
        data = json_load(self.path)

        super().__init__(data, *args, **kwargs)

    def __setitem__(self, key: str, value: Any):
        super().__setitem__(key, value)
        self.dump()

    def __delitem__(self, key: str):
        super().__delitem__(key)
        self.dump()

    def dump(self):
        """Dump the dictionary to a JSON file.

        Args:
        ----
            path (str): The path to the file to which the dictionary will be written.

        Returns:
        -------
            None
        """
        json_dump(self, self.path)
