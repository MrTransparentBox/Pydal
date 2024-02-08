"""Provides artist data types"""

from .base import BaseType
from .media import Picture


class Artist(BaseType):
    """Base artist API type"""

    id: str
    name: str
    picture: list[Picture]


class FullArtist(Artist):
    """Artist with URL as given by /artists"""

    tidalUrl: str


class NestedArtist(Artist):
    """Artist as given in track artists"""

    main: bool
