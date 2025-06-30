from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "mini-rag-system"
    debug: bool = True

settings = Settings() 