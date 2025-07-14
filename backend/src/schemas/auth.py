from pydantic import BaseModel, EmailStr, ConfigDict


class _BaseUserModel(BaseModel):
    username: str
    password: str


class UserCreate(_BaseUserModel):
    email: EmailStr

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "global_lectures",
                "password": "1234",
                "email": "donotreply@global.lectures"
            }
        }
    )


class UserLogin(_BaseUserModel):
    pass

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "global_lectures",
                "password": "1234"
            }
        }
    )
