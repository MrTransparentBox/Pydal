"""Provides main client class"""

from typing import Sequence

import httpx

from .models import *
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

    async def _api_call(self, url: str) -> dict:
        response = await self.http.get(
            url,
            headers=self.default_headers,
        )
        response.raise_for_status()
        return response.json()

    async def track(self, id: str, countryCode: str) -> Track:
        """Requests to the /tracks/{id} endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return (await self._api_call(f"/tracks/{id}?countryCode={countryCode}"))["resource"]

    async def many_tracks(self, ids: Sequence[str], countryCode: str) -> ExpandedDataItems[Track]:
        """Requests to the /tracks?ids={ids} endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return await self._api_call(f"/tracks?ids={'%2C'.join(ids)}&countryCode={countryCode}")

    async def similar_tracks(self, id: str, countryCode: str, offset: int = 0, limit: int = 10) -> DataItems:
        """/tracks/{id}/similar.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code"""
        return await self._api_call(f"/tracks/{id}/similar?countryCode={countryCode}&offset={offset}&limit={limit}")

    async def tracks_isrc(self, isrc: str, countryCode: str) -> Track:
        """Requests to the /tracks/{id} endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return (await self._api_call(f"/tracks/byIsrc?isrc={isrc}&countryCode={countryCode}"))["data"][0]["resource"]

    async def video(self, id: str, countryCode: str) -> Video:
        """Requests to the /videos/{id} endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return (await self._api_call(f"/videos/{id}?countryCode={countryCode}"))["resource"]

    async def many_videos(self, ids: Sequence[str], countryCode: str) -> ExpandedDataItems[Video]:
        """Requests to the /tracks?ids={ids} endpoint.
        Raises:
            HTTPStatusError: HTTP request didn't return 2xx code
        """
        return await self._api_call(f"/videos?ids={'%2C'.join(ids)}&countryCode={countryCode}")
