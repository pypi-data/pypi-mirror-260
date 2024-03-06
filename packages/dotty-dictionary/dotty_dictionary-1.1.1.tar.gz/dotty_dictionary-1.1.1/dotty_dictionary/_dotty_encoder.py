import json
from typing import Any


class DottyEncoder(json.JSONEncoder):
    """Helper class for encoding of nested Dotty dicts into standard dict"""

    def default(self, obj: Any) -> Any:
        """Return dict data of Dotty when possible or encode with standard format

        Parameters:
            obj: Input object

        Returns:
            Serializable data
        """
        if hasattr(obj, "_data"):
            return obj._data
        else:
            return json.JSONEncoder.default(self, obj)
