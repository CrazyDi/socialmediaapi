from typing import Optional
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None

    class Config:
        env_file: str = ".env"
        extra: str = "allow"


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False
    MAILGUN_DOMAIN: Optional[str] = None
    MAILGUN_API_KEY: Optional[str] = None
    DEEPAI_API_KEY: Optional[str] = None


class DevConfig(GlobalConfig):
    class Config:
        env_prefix: str = "DEV_"


class ProdConfig(GlobalConfig):
    class Config:
        env_prefix: str = "PROD_"


class TestConfig(GlobalConfig):
    DATABASE_URL: Optional[str] = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True

    class Config:
        env_prefix: str = "TEST_"


@lru_cache()
def get_config(env_state: str):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)
