from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    PROJECT_NAME: str = "Credit API"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

try:
    settings = Settings()
except ValueError as e:
    raise ValueError(f"Error while reading environment variable: {e}")