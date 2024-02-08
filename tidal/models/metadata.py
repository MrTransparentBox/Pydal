"""Metadata types in raw requests"""

from .base import BaseType


class MediaMetadata(BaseType):
    """Raw request metadata for media"""

    tags: list[str]


class Metadata(BaseType):
    """Request metadata"""

    requested: int
    success: int
    failure: int
    total: int
