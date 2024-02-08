from typing import Literal

from .album import Album
from .artist import NestedArtist
from .base import BaseType
from .picture import Picture
from .properties import Properties


class Video(BaseType):
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
