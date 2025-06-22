from pydantic import field_validator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    POSTGRES_DSN: PostgresDsn | None = None

    model_config = SettingsConfigDict(
        env_file="../envs/.env.database",
        env_file_encoding='utf-8'
    )

    @field_validator("POSTGRES_DNS", mode="before")
    @classmethod
    def db_dsn(cls, v, info):
        if v is not None:
            return v

        values = info.data

        return (
            f"postgresql://{values['POSTGRES_USER']}:{values['POSTGRES_PASSWORD']}"
            f"@{values['POSTGRES_HOST']}:{values['POSTGRES_PORT']}/{values['POSTGRES_NAME']}"
        )


database_settings = DatabaseSettings()
