from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    jwt_secret: str = "change-me"
    database_url: str = "sqlite+aiosqlite:///./sellerai.db"

    model_config = {"env_file": ".env"}


settings = Settings()
