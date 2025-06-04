from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session

from src.db.postgres import get_db
from src.auth.jwt_handler import verify_access_token


async def authenticate(request: Request, db: Session = Depends(get_db)) -> dict[str, str | int]:
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token not exist"
        )
    decoded_token: dict = await verify_access_token(token, db)
    return {"user": decoded_token["user"], "id": decoded_token["id"]}
