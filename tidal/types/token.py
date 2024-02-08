"""Data structure for stored access tokens"""

import datetime


class Token:
    access_token: str
    token_type: str
    retrieved: datetime.datetime
    expires_in: datetime.timedelta

    def __init__(self, access_token: str, token_type: str, expires_in: int) -> None:
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = datetime.timedelta(seconds=expires_in)
        self.retrieved = datetime.datetime.utcnow()

    def is_valid(self) -> bool:
        return self.retrieved + self.expires_in < datetime.datetime.utcnow()
