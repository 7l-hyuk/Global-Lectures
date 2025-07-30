from pydantic import field_validator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str
    POSTGRES_DSN: PostgresDsn | None = None

    @field_validator("POSTGRES_DSN", mode="before")
    @classmethod
    def db_dsn(cls, v, info):
        if v is not None:
            return v

        psql_config = info.data
        return (
            f"postgresql://{psql_config['POSTGRES_USER']}"
            f":{psql_config['POSTGRES_PASSWORD']}"
            f"@{psql_config['POSTGRES_HOST']}"
            f":{psql_config['POSTGRES_PORT']}"
            f"/{psql_config['POSTGRES_DB']}"
        )


class JWTSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


class RedisSettings(BaseSettings):
    REDIS_DSN: str


class AwsSettings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    BUCKET_NAME: str
    REGION: str


class ApiSettings(BaseSettings):
    GPT_API_KEY: str
    XI_API_KEY: str
    STT_SERVER_URL: str
    TRANSLATION_SERVER_URL: str
    TTS_SERVER_URL: str
    REDIS_DSN: str


database_settings = DatabaseSettings()
jwt_settings = JWTSettings()
redis_settings = RedisSettings()
aws_settings = AwsSettings()
api_settings = ApiSettings()
