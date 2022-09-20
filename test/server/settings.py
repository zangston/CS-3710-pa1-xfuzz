# Settings for the test server.

import random
import hmac
import secrets
import xfuzz._typing as _t
from pydantic import BaseSettings, Field
from test.wordlists import get_common


def create_token(key: bytes, msg: str) -> bytes:
    """Generate a new cryptographically random token using HMAC-SHA256."""

    msg = msg.encode("utf-8")
    return hmac.new(key, msg=msg, digestmod="sha256").digest()


class Settings(BaseSettings):
    """Configuration options for the test server."""

    class Config:
        allow_mutation = False
        extra = "forbid"

    # The OpenAPI configuratoin URL.
    openapi_url: str = "/openapi.json"

    # Wordlist to pass in to xfuzz and to use for testing configuration
    wordlist: _t.List[str] = Field(default_factory=get_common)

    # A secret token that can be used to generate additional secret tokens
    key: bytes = Field(default_factory=secrets.token_bytes)

    def create_token(self, msg: str) -> bytes:
        return create_token(self.key, msg)

    def create_token_int(self, msg: str) -> int:
        return int.from_bytes(self.create_token(msg), "little")

    def random_word(self, token_msg: str) -> str:
        """Select a random word from the wordlist after seeding the RNG with a value
        deterministically generated from the input token message."""

        random.seed(self.create_token_int(token_msg))
        return random.choice(self.wordlist)

    def ext_router_endpoint(self) -> str:
        return self.random_word("ext-router-endpoint")

    def auth_router_password(self) -> str:
        return self.random_word("auth-router-password")
