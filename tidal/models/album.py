from typing import Literal

from .artist import NestedArtist
from .base import BaseType
from .metadata import MediaMetadata
from .picture import Picture
from .properties import Properties


class Album(BaseType):
    id: str
    title: str
    imageCover: list[Picture]
    videoCover: list[Picture]


class FullAlbum(Album):
    barcodeId: str
    artists: list[NestedArtist]
    duration: int
    releaseDate: str
    numberOfVolumes: int
    numberOfTracks: int
    numberOfVideos: int
    type: Literal["ALBUM"]
    copyright: str
    mediaMetadata: MediaMetadata
    properties: Properties
    tidalUrl: str
