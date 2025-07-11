from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    github_token: str
    github_webhook_secret: str
    openai_api_key: str
    openai_model: str = "gpt-4"
    port: int = 8000
    host: str = "0.0.0.0"
    environment: str = "development"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()