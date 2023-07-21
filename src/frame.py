import numpy as np
from typing import Any
from datetime import datetime

class Frame:
    """Data structure to hold video frames and their timestamp."""

    def __init__(self, current_frame, next_frame, metadata: dict[str, Any] = None):
        self.timestamp = datetime.now()
        self.current_frame = current_frame
        self.next_frame = next_frame
        self._metadata = metadata or {}

    def __getitem__(self, key: str) -> Any:
        """Retrieve value for a given key from metadata."""
        return self._metadata[key]

    def __setitem__(self, key: str, value: Any):
        """Set a value for a given key in metadata."""
        self._metadata[key] = value

    @property
    def metadata(self) -> dict[str, Any]:
        """Getter for metadata."""
        return self._metadata

    def array(self) -> np.array:
        return self.current_frame
