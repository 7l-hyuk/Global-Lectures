from pydantic import field_validator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str
    POSTGRES_DSN: PostgresDsn = None

    model_config = SettingsConfigDict(
        env_file="../envs/.env.database",
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

database_settings = DatabaseSettings()
print(database_settings.POSTGRES_DSN)
jwt_settings = JWTSettings()
