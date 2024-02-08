"""Provides video API model"""

from typing import Literal

from .album import Album
from .artist import NestedArtist
from .base import BaseType
from .media import Picture
from .resource import Properties


class Video(BaseType):
    """Video API dict type"""

    artifactType: Literal["video"]
    id: str
    title: str
    image: list[Picture]
    releaseDate: str
    artists: list[NestedArtist]
    duration: int
    trackNumber: int
    volumeNumber: int
    album: Album
    isrc: str
    copyright: str | None
    tidalUrl: str
    properties: Properties
    version: str | None
