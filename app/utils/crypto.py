import secrets


def gen_id(size: int = 32) -> str:
    return secrets.token_urlsafe(size)
