from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from src.config import jwt_settings
from src.schema.user import User


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


async def verify_access_token(
    token: str,
    db: Session
) -> dict:
    try:
        data = jwt.decode(
            token=token,
            key=jwt_settings.SECRET_KEY,
            algorithms=jwt_settings.ALGORITHM
        )
        expire = data.get("exp")

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
                detail="Token expired!"
            )

        is_user_exist = db.query(User).filter(User.username == data["user"]).first()
        if not is_user_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token"
            )
        return data

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )