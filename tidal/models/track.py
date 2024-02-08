from typing import Literal

from .album import Album
from .artist import NestedArtist
from .base import BaseType
from .metadata import MediaMetadata
from .properties import Properties


class Track(BaseType):
    artifactType: Literal["track"]
    id: str
    title: str
    artists: list[NestedArtist]
    album: Album
    duration: int
    trackNumber: int
    volumeNumber: int
    isrc: str
    copyright: str
    mediaMetadata: MediaMetadata
    properties: Properties
    tidalUrl: str
