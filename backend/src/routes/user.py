from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
import bcrypt

from src.db.postgres import get_db
from src.db.user import User
from src.schema.user import UserCreate, UserLogin, UserUpdate
from src.auth.jwt_handler import create_access_token
from src.services.user import get_current_user
from src.auth.authenticate import authenticate

user_router = APIRouter(prefix="/api/users", tags=["Users"])


@user_router.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(username=user.username, password=hashed_pw.decode(), email=user.email)
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=200, detail="이미 존재하는 사용자입니다.")
    return {"msg": "회원가입 완료!", "username": user.username}


@user_router.post("/login")
async def user_login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if (
        not db_user 
        or not bcrypt.checkpw(
            user.password.encode("utf-8"),
            db_user.password.encode()
        )
    ):
        raise HTTPException(status_code=200, detail="잘못된 로그인 정보입니다.")

    access_token = create_access_token(data={"user": db_user.username, "id": db_user.id})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,         # 개발환경에서는 False, 운영에서는 반드시 True
        samesite="lax",        # CSRF 방어용
        path="/"
    )
    return {"msg": "login success"}


@user_router.get("/me")
async def read_users_me(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=200, detail="토큰이 없습니다.")

    current_user = get_current_user(token)
    return {"username": current_user}


@user_router.post("/logout")
async def user_logout(response: Response):
    response.delete_cookie("access_token", path="/")
    return {"msg": "logout success"}


@user_router.patch("/update")
async def update_user(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(authenticate)
):
    return ...