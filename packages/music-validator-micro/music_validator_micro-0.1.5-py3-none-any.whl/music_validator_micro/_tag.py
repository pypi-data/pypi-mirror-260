"""
Provides tag class
"""
from dataclasses import dataclass


@dataclass
class Tag():
    """
    Represents a tag in a music file, provides a link between
    the internal naming scheme of a tag to a human readable
    format
    """

    value: str
    internal_name: str
    external_name: str
