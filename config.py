from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path

# Get the root directory
ROOT_DIR = Path(__file__).parent

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DEBUG: bool = False
    
    class Config:
        env_file = ROOT_DIR / ".env"

@lru_cache()
def get_settings():
    return Settings()