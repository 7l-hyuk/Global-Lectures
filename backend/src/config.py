from pydantic import field_validator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str
    POSTGRES_DSN: PostgresDsn | None = None

    model_config = SettingsConfigDict(
        env_file="../envs/.env.psql",
        env_file_encoding='utf-8'
    )

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

    model_config = SettingsConfigDict(
        env_file="../envs/.env.jwt",
        env_file_encoding='utf-8'
    )


class RedisSettings(BaseSettings):
    REDIS_DSN: str

    model_config = SettingsConfigDict(
        env_file="../envs/.env.redis",
        env_file_encoding='utf-8'
    )


class AwsSettings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    BUCKET_NAME: str
    REGION: str

    model_config = SettingsConfigDict(
        env_file="../envs/.env.aws",
        env_file_encoding='utf-8'
    )


class ApiSettings(BaseSettings):
    GPT_API_KEY: str
    XI_API_KEY: str
    STT_SERVER_URL: str
    TRANSLATION_SERVER_URL: str
    TTS_SERVER_URL: str
    REDIS_DSN: str

    model_config = SettingsConfigDict(
        env_file="../envs/.env.api",
        env_file_encoding='utf-8'
    )


database_settings = DatabaseSettings()
jwt_settings = JWTSettings()
redis_settings = RedisSettings()
aws_settings = AwsSettings()
api_settings = ApiSettings()
