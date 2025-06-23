from pydantic import BaseModel, EmailStr


class _BaseUserModel(BaseModel):
    username: str
    password: str


class UserCreate(_BaseUserModel):
    email: EmailStr


class UserLogin(_BaseUserModel):
    pass


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None
