from .base import BaseType


class MediaMetadata(BaseType):
    tags: list[str]


class Metadata(BaseType):
    requested: int
    success: int
    failure: int
    total: int
