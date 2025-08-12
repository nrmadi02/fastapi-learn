from datetime import UTC, datetime, timedelta

import jwt

from app.core.config import settings


def create_access_token(subject: str) -> str:
    now = datetime.now(UTC)
    exp = now + timedelta(minutes=settings.jwt_expires_minutes)
    payload = {"sub": subject, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(
        payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def decode_token(token: str) -> dict:
    return jwt.decode(
        token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
    )
