from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    yandex_api_key: str = ""
    yandex_folder_id: str = ""
    jwt_secret: str = "change-me"
    database_url: str = "sqlite+aiosqlite:///./sellerai.db"
    google_client_id: str = ""
    google_client_secret: str = ""
    vk_client_id: str = ""
    vk_client_secret: str = ""
    yandex_client_id: str = ""
    yandex_client_secret: str = ""
    frontend_url: str = "http://localhost:5500"

    model_config = {"env_file": ".env"}


settings = Settings()
