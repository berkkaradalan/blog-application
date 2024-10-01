import os
from dotenv import load_dotenv
from pydantic import BaseModel
# from pydantic_settings import BaseSettings
#! ModuleNotFoundError: No module named 'pydantic_settings'

load_dotenv()

class Settings(BaseModel):
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    MONGO_USERNAME: str = os.getenv("MONGO_USERNAME")
    MONGO_PASSWORD: str = os.getenv("MONGO_PASSWORD")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_TIME: int = os.getenv("ACCESS_TOKEN_EXPIRE_TIME", 99999)
    CORS_ALLOWED_ORIGINS: list = os.getenv("CORS_ALLOWED_ORIGINS")
    MONGO_IP: str = os.getenv("MONGO_IP")
    MONGO_PORT: int = os.getenv("MONGO_PORT", 27017)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()