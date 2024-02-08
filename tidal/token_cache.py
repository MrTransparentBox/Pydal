import os
import pickle

import httpx

from .types.token import Token


class TokenCache:
    def __init__(self, auth: httpx.BasicAuth) -> None:
        self.token: Token | None = None
        self._auth = auth
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
        response = self.http.post(
            url="https://auth.tidal.com/v1/oauth2/token",
            headers={
                "Authorization": self._auth._auth_header,
                "Content-type": "application/x-www-form-urlencoded",
                "Accept": "application/json,text/plain",
            },
            data="grant_type=client_credentials",
        )
        response.raise_for_status()
        data: dict = response.json()
        self.token = Token(
            access_token=data["access_token"],
            token_type=data["token_type"],
            expires_in=data["expires_in"],
        )
        self._write_cache()

    def get_token(self) -> Token:
        if self.token and not self.token.is_valid():
            self._request_token()
        if not self.token and not self._read_cache():
            self._request_token()
        return self.token
