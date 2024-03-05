from datetime import timedelta

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class DefaultSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    LOGGER_FORMAT_STRING: str = "%(asctime)s | %(levelname)7s | %(thread)s | %(module)30s : %(message)s"

    # DB
    SQLALCHEMY_ECHO: bool = False
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"

    # CACHE
    CACHE_TYPE: str = "SimpleCache"

    # JWT
    JWT_ACCESS_TOKEN_EXPIRES: int | timedelta = timedelta(hours=1)
