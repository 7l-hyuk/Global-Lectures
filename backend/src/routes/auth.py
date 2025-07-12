from fastapi import APIRouter, Depends, HTTPException, status, Response, Request

from sqlalchemy.orm import Session

from src.schemas.auth import UserCreate, UserLogin
from src.database.tables import User
from src.database.postgres import get_db
from src.auth.hash_handler import create_hash, verify_hash
from src.auth.jwt_handler import create_access_token, verify_acess_token
from src.services.auth import get_current_user


auth_router = APIRouter(prefix="/api/auth", tags=["Auth"])


@auth_router.post("/signup")
def sign_up(
    user: UserCreate,
    db: Session = Depends(get_db)
) -> dict[str, str]:
    hashed_password = create_hash(user.password)
    new_user = User(
        username=user.username,
        password=hashed_password,
        email=user.email
    )
    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="User already exist"
        )
    return {
        "msg": "Sign up completed successfully",
        "username": user.username
    }


@auth_router.post("/signin")
def sign_in(
    user: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
) -> dict[str, str]:
    db_user = db.query(User).filter(User.username == user.username).first()

    if (
        not db_user
        or not verify_hash(
            plain_password=user.password,
            hashed_password=db_user.password
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    access_token = create_access_token(
        payload={"id": db_user.id, "username": db_user.username}
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )
    return {"msg": "Login Success"}


@auth_router.get("/me")
def check_me(request: Request) -> dict[str, str]:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not Login"
        )
    current_user_name = get_current_user(access_token=access_token)
    return {"username": current_user_name}


@auth_router.post("/signout")
def sign_out(response: Response):
    response.delete_cookie("access_token", path="/")
    return {"msg": "User sign out success"}
