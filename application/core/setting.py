from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    PROJECT_NAME: str = "Credit API"

try:
    settings = Settings()
except Exception as e:
    raise f"Error while reading enviornment variable {e}"