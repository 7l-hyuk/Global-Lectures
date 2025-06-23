from fastapi import HTTPException, status
from jose import jwt, JWTError
from src.config import jwt_settings


def get_current_user(access_token: str) -> str:
    try:
        payload = jwt.decode(
            token=access_token,
            key=jwt_settings.SECRET_KEY,
            algorithms=jwt_settings.ALGORITHM
        )
        username = payload.get("username")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authenticaion payload",
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticaion failed"
        )