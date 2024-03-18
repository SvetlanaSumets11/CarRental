from datetime import timedelta

from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer

from app.core.config import get_settings

ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=30)

access_security = JwtAccessBearer(
    get_settings().AUTH_JWT_SECRET_KEY,
    access_expires_delta=ACCESS_EXPIRES,
    refresh_expires_delta=REFRESH_EXPIRES,
)

refresh_security = JwtRefreshBearer(
    get_settings().AUTH_JWT_SECRET_KEY,
    access_expires_delta=ACCESS_EXPIRES,
    refresh_expires_delta=REFRESH_EXPIRES,
)


def get_jwt_subject(email: str) -> dict[str, str]:
    return {'username': email}
