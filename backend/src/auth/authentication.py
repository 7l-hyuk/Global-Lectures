from dataclasses import dataclass

from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.unit_of_work import get_uow, UnitOfWork
from src.auth.jwt_handler import verify_acess_token

JWTPayload = dict[str, str | int]


@dataclass
class AuthenticatedPayload:
    id: int
    username: str


async def authenticate(
    request: Request,
    uow: UnitOfWork = Depends(get_uow)
) -> JWTPayload:
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No access token supplied",
        )
    with uow as u:
        payload: JWTPayload = verify_acess_token(
            access_token=token,
            uow=u
        )
        return AuthenticatedPayload(
            id=payload["id"],
            username=payload["username"]
        )
