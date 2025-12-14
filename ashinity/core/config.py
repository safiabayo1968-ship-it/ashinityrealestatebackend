from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = Field(default="Ashinity Real Estate API")
    ENV: str = Field(default="development")
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)
    CORS_ORIGINS: str = Field(default="*")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
