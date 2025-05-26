from datetime import datetime, timedelta, timezone

from jose import jwt

from src.config import jwt_settings


def create_access_token(data: dict, expires_delta: int =None):
    to_encode = data.copy()
    expire = (
        datetime.now(timezone.utc) 
        + (
            expires_delta 
            or timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=jwt_settings.SECRET_KEY,
        algorithm=jwt_settings.ALGORITHM
    )
    return encoded_jwt

