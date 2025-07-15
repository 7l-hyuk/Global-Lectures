from dataclasses import dataclass

from fastapi import Request, Depends, HTTPException, status

from src.models.unit_of_work import get_uow, UnitOfWork
from src.auth.jwt_handler import verify_acess_token, JWTPayload


@dataclass
class AuthenticatedPayload:
    id: int
    username: str


def authenticate(
    request: Request,
    uow: UnitOfWork = Depends(get_uow)
) -> AuthenticatedPayload:
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
