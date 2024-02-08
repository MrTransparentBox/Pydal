"""Provides main client class"""

from typing import Iterable

import httpx

from .models import (
    BaseType,
    DataItems,
    ExpandedDataItems,
    ExpandedResource,
    FullAlbum,
    FullArtist,
    Track,
    Video,
)
from .token_cache import TokenCache


class TidalClient:
    """Base client class"""

    def __init__(self, client_id, client_secret) -> None:
        self._auth = httpx.BasicAuth(client_id, client_secret)
        self._cache = TokenCache(self._auth)
        self._http: httpx.AsyncClient = None

    @property
    def http(self):
        if self._http is None:
            self._http = httpx.AsyncClient(
                http2=True,
                follow_redirects=True,
                base_url="https://openapi.tidal.com",
            )
        return self._http

    @property
    def default_headers(self):
        return {
            "accept": "application/vnd.tidal.v1+json",
            "Content-Type": "application/vnd.tidal.v1+json",
            "Authorization": f"Bearer {self._cache.get_token().access_token}",
        }

    async def _api_call(self, url: str) -> BaseType:
        response = await self.http.get(
            url,
            headers=self.default_headers,
        )
        response.raise_for_status()
        return response.json()

    # region albums
    async def album(self, album_id: str, country_code: str) -> FullAlbum:
        """Requests to the /albums/{id} endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return await self._api_call(f"/albums/{album_id}?countryCode={country_code}")["resource"]

    async def many_albums(self, ids: Iterable[str], country_code: str) -> ExpandedDataItems[FullAlbum]:
        """Requests to the /albums?ids={ids} endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return await self._api_call(f"/artists?ids={'%2C'.join(ids)}&countryCode={country_code}")

    async def album_items(
        self, album_id: str, country_code: str, offset: int = 0, limit: int | None = None
    ) -> ExpandedDataItems[Track]:
        """Requests to the /albums/{id}/items endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        url = f"/albums/{album_id}/items?countryCode={country_code}&offset={offset}"
        if limit is not None:
            url += f"&limit={limit}"
        return await self._api_call(url)

    async def album_by_barcode(self, barcode_id: str, country_code: str) -> FullAlbum:
        """Requests to the /albums/byBarcodeId?barcodeId={barcode_id} endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        result: ExpandedDataItems[FullAlbum] = await self._api_call(
            f"/albums/byBarcodeId?barcodeId={barcode_id}&countryCode={country_code}"
        )
        return result["data"][0]["resource"]

    async def similar_albums(self, album_id: str, country_code: str, offset: int = 0, limit: int = 10) -> DataItems:
        """Requests to the /albums/{id}/similar endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return await self._api_call(
            f"/albums/{album_id}/similar?countryCode={country_code}&offset={offset}&limit={limit}"
        )

    async def albums_by_artist(
        self, artist_id: str, country_code: str, offset: int = 0, limit: int = 10
    ) -> ExpandedDataItems[FullAlbum]:
        """Requests to the /artists/{id}/albums endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return await self._api_call(
            f"/artists/{artist_id}/albums?countryCode={country_code}&offset={offset}&limit={limit}"
        )

    # endregion
    # region artists
    async def artist(self, artist_id: str, country_code: str) -> FullArtist:
        """Requests to the /artists/{id} endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        result: ExpandedResource[FullArtist] = await self._api_call(f"/artists/{artist_id}?countryCode={country_code}")
        return result["resource"]

    async def many_artists(self, ids: Iterable[str], country_code: str) -> ExpandedDataItems[FullArtist]:
        """Requests to the /artists?ids={ids} endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return await self._api_call(f"/artists?ids={'%2C'.join(ids)}&countryCode={country_code}")

    async def similar_artists(self, artist_id: str, country_code: str, offset: int = 0, limit: int = 10) -> DataItems:
        """Requests to the /artists/{id}/similar endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return await self._api_call(
            f"/artists/{artist_id}/similar?countryCode={country_code}&offset={offset}&limit={limit}"
        )

    # endregion
    # region tracks
    async def track(self, track_id: str, country_code: str) -> Track:
        """Requests to the /tracks/{id} endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return (await self._api_call(f"/tracks/{track_id}?countryCode={country_code}"))["resource"]

    async def many_tracks(self, ids: Iterable[str], country_code: str) -> ExpandedDataItems[Track]:
        """Requests to the /tracks?ids={ids} endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return await self._api_call(f"/tracks?ids={'%2C'.join(ids)}&countryCode={country_code}")

    async def similar_tracks(self, track_id: str, country_code: str, offset: int = 0, limit: int = 10) -> DataItems:
        """Requests to the /tracks/{id}/similar endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code"""
        return await self._api_call(
            f"/tracks/{track_id}/similar?countryCode={country_code}&offset={offset}&limit={limit}"
        )

    async def tracks_isrc(self, isrc: str, country_code: str) -> Track:
        """Requests to the /tracks/{id} endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return (await self._api_call(f"/tracks/byIsrc?isrc={isrc}&countryCode={country_code}"))["data"][0]["resource"]

    # endregion
    # region video

    async def video(self, track_id: str, country_code: str) -> Video:
        """Requests to the /videos/{id} endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return (await self._api_call(f"/videos/{track_id}?countryCode={country_code}"))["resource"]

    async def many_videos(self, ids: Iterable[str], country_code: str) -> ExpandedDataItems[Video]:
        """Requests to the /tracks?ids={ids} endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return await self._api_call(f"/videos?ids={'%2C'.join(ids)}&countryCode={country_code}")


# endregion
