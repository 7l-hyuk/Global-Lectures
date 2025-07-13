from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.config import jwt_settings    
from src.database.tables import User
from src.database.unit_of_work import UnitOfWork


def create_access_token(payload: dict, expires_delta: int = None):
    to_encode = payload.copy()
    to_encode["exp"] = datetime.now(timezone.utc) 
    + (
        expires_delta 
        or timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return jwt.encode(
        claims=to_encode,
        key=jwt_settings.SECRET_KEY,
        algorithm=jwt_settings.ALGORITHM
    )


def verify_acess_token(
    access_token: str,
    uow: UnitOfWork
) -> dict:
    try:
        payload = jwt.decode(
            token=access_token,
            key=jwt_settings.SECRET_KEY,
            algorithms=jwt_settings.ALGORITHM
        )
        expire = payload.get("exp")

        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied"
            )
        if (
            datetime.now(timezone.utc) 
            > datetime.fromtimestamp(expire, tz=timezone.utc)
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access token was expired"
            )
        user = uow.users.get_user_by_id(payload["id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )
