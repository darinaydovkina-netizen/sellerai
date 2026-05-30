from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    yandex_api_key: str = ""
    yandex_folder_id: str = ""
    jwt_secret: str = "change-me"
    database_url: str = "sqlite+aiosqlite:///./sellerai.db"

    model_config = {"env_file": ".env"}


settings = Settings()
