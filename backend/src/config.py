from dataclasses import dataclass

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


@dataclass
class BaseModelConfig:
    model_config = model_config = ConfigDict(
        env_file=".env", 
        extra="ignore"
    )


class DatabaseSettings(BaseSettings, BaseModelConfig):
    DATABASE_URL: str | None = None


class JwtSettings(BaseSettings, BaseModelConfig):
    SECRET_KEY: str | None = None
    ALGORITHM: str | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int | None = None


class AwsSettings(BaseSettings, BaseModelConfig):
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    BUCKET_NAME: str | None = None
    REGION: str | None = None


class ServiceSettings(BaseSettings, BaseModelConfig):
    GPT_API_KEY: str | None = None
    XI_API_KEY: str | None = None


database_settings = DatabaseSettings()
jwt_settings = JwtSettings()
aws_settings = AwsSettings()
service_settings = ServiceSettings()
