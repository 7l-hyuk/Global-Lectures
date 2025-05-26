from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
import bcrypt

from src.db.database import get_db
from src.schema.users import User, UserCreate, UserLogin
from src.auth.jwt_handler import create_access_token
from src.services.users import get_current_user


users_router = APIRouter(prefix="/api/users", tags=["users"])


@users_router.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(username=user.username, hashed_password=hashed_pw.decode(), email=user.email)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자입니다.")
    return {"msg": "회원가입 완료!", "username": user.username}


@users_router.post("/login")
async def user_login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if (
        not db_user 
        or not bcrypt.checkpw(
            user.password.encode("utf-8"),
            db_user.hashed_password.encode()
        )
    ):
        raise HTTPException(status_code=401, detail="잘못된 로그인 정보입니다.")

    access_token = create_access_token(data={"sub": user.username})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,         # 개발환경에서는 False, 운영에서는 반드시 True
        samesite="lax",        # CSRF 방어용
        path="/"
    )

    return {"msg": "login success"}


@users_router.get("/me")
async def read_users_me(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="토큰이 없습니다.")
    
    current_user = get_current_user(token)
    return {"username": current_user}


@users_router.post("/logout")
def user_logout(response: Response):
    response.delete_cookie("access_token", path="/")
    return {"msg": "logout success"}
