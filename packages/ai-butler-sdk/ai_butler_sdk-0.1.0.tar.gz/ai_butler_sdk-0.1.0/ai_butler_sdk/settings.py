from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AI_BUTLER_SDK_BASE_URL: str = ""


@lru_cache
def get_settings() -> Settings:
    """读取配置优化写法, 全局共享"""
    return Settings()  # type: ignore


settings = get_settings()
