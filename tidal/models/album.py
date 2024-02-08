"""Album api models"""

from typing import Literal

from .artist import NestedArtist
from .base import BaseType
from .media import Picture
from .metadata import MediaMetadata
from .resource import Properties


class Album(BaseType):
    """Base album type for track requests"""

    id: str
    title: str
    imageCover: list[Picture]
    videoCover: list[Picture]


class FullAlbum(Album):
    """Full album info as given in /albums requests"""

    barcodeId: str
    artists: list[NestedArtist]
    duration: int
    releaseDate: str
    numberOfVolumes: int
    numberOfTracks: int
    numberOfVideos: int
    type: Literal["ALBUM"] | Literal["SINGLE"]
    copyright: str
    mediaMetadata: MediaMetadata
    properties: Properties
    tidalUrl: str
