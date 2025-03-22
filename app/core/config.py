from functools import lru_cache
from typing import Any, Optional

from pydantic import PostgresDsn
from pydantic.functional_validators import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Role Based Access Control Auth Service"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    USERS_OPEN_REGISTRATION: str

    ENVIRONMENT: Optional[str]

    FIRST_SUPER_ADMIN_EMAIL: str
    FIRST_SUPER_ADMIN_PASSWORD: str
    FIRST_SUPER_ADMIN_ACCOUNT_NAME: str

    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode='after')
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: Any) -> Optional[str]:
        if v is not None:
            return v

        data = info.data  # ✅ get the data from ValidationInfo

        return PostgresDsn.build(
            scheme="postgresql",
            username=data["DB_USER"],
            password=data["DB_PASSWORD"],
            host=data["DB_HOST"],
            port=5432,
            path=f"{data['DB_NAME']}",
        ).__str__()

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
