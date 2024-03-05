import secrets

from passlib.context import CryptContext

from . import config

pwd_context = CryptContext(schemes=["argon2"])


def generate_secret_token() -> str:
    """Helper for generating a secret key."""
    return secrets.token_hex(config.settings.secret_key_n_bytes)
