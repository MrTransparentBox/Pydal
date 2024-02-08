"""Utilities for retrieval and storage of access tokens"""

import os
import pickle

import httpx

from .types.token import Token


class TokenCache:
    """Stores and retrieves access tokens, requests new tokens upon expiry.\n
    Get active token using `.get_token()`"""

    def __init__(self, auth: httpx.BasicAuth) -> None:
        self.token: Token | None = None
        self.auth = auth
        self.http = httpx.Client(http2=True, follow_redirects=True)

    def _read_cache(self) -> bool:
        """Attemps to read cache and returns whether the operation was succesful. Sets self.token"""
        if not os.path.exists(".token_cache"):
            return False
        with open(".token_cache", "rb") as f:
            try:
                self.token = pickle.load(f)
            except ModuleNotFoundError:
                os.remove(".token_cache")
                return False
            return True

    def _write_cache(self):
        if not self.token:
            return
        with open(".token_cache", "wb") as f:
            pickle.dump(self.token, f, pickle.HIGHEST_PROTOCOL)

    def _request_token(self):
        request = self.http.build_request(
            "POST",
            "https://auth.tidal.com/v1/oauth2/token",
            data="grant_type=client_credentials",
            headers={
                "Content-type": "application/x-www-form-urlencoded",
                "Accept": "application/json,text/plain",
            },
        )
        print(request.url)
        response = self.http.send(request, auth=self.auth)
        response.raise_for_status()
        data: dict = response.json()
        self.token = Token(
            access_token=data["access_token"],
            token_type=data["token_type"],
            expires_in=data["expires_in"],
        )
        self._write_cache()

    def get_token(self) -> Token:
        if not self.token and not self._read_cache():
            self._request_token()
        if self.token and not self.token.is_valid():
            self._request_token()
        return self.token
