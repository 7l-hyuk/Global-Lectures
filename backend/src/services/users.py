from fastapi import HTTPException, status
from jose import jwt, JWTError

from src.config import jwt_settings


def get_current_user(token):
    try:
        payload = jwt.decode(
            token=token,
            key=jwt_settings.SECRET_KEY,
            algorithms=jwt_settings.ALGORITHM
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 인증 정보입니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰 인증 실패",
            headers={"WWW-Authenticate": "Bearer"},
        )
