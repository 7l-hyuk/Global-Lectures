from pydantic import ConfigDict
from pydantic_settings import BaseSettings

model_config = ConfigDict(
    env_file=".env", 
    extra="ignore"
)

class DatabaseSettings(BaseSettings):
    DATABASE_URL: str | None = None

    model_config = model_config


class JwtSettings(BaseSettings):
    SECRET_KEY: str | None = None
    ALGORITHM: str | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int | None = None

    model_config = model_config


database_settings = DatabaseSettings()
jwt_settings = JwtSettings()