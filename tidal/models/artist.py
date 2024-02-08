from .base import BaseType
from .picture import Picture


class Artist(BaseType):
    id: str
    name: str
    picture: list[Picture]


class FullArtist(Artist):
    tidalUrl: str


class NestedArtist(Artist):
    main: bool
