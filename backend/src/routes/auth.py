from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from jose import jwt, JWTError
from src.config import jwt_settings

from src.schemas.auth import UserCreate, UserLogin
from src.models.tables import User
from src.models.unit_of_work import get_uow
from src.models.unit_of_work import UnitOfWork
from src.auth.hash_handler import create_hash, verify_hash
from src.auth.jwt_handler import create_access_token

auth_router = APIRouter(prefix="/api/auth", tags=["Auth"])


@auth_router.post("/signup")
def sign_up(
    user: UserCreate,
    uow: UnitOfWork = Depends(get_uow)
) -> dict[str, str]:
    try:
        with uow as u:
            hashed_password = create_hash(user.password)
            new_user = User(
                username=user.username,
                password=hashed_password,
                email=user.email
            )
            u.users.add(new_user)
        return {
            "msg": "Sign up completed successfully",
            "username": user.username
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="User already exist"
        )


@auth_router.post("/signin")
def sign_in(
    user: UserLogin,
    response: Response,
    uow: UnitOfWork = Depends(get_uow)
) -> dict[str, str]:
    try:
        with uow as u:
            db_user = u.users.get_user_by_name(user.username)
            if (
                not db_user
                or not verify_hash(
                    plain_password=user.password,
                    hashed_password=db_user.password
                )
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            access_token = create_access_token(
                payload={
                    "id": db_user.id,
                    "username": db_user.username
                }
            )
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="lax",
                path="/"
            )
            return {"msg": "Login success"}
    except Exception as e:
        print(e)


@auth_router.get("/me")
def check_me(request: Request) -> dict[str, str]:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not Login"
        )
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
        return {"username": username}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticaion failed"
        )


@auth_router.post("/signout")
def sign_out(response: Response):
    response.delete_cookie("access_token", path="/")
    return {"msg": "User sign out success"}
