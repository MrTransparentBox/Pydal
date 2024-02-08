"""Data classes for media """

from .base import BaseType


class Picture(BaseType):
    """Image metadata"""

    url: str
    width: int
    height: int
