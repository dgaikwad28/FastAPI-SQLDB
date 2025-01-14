import os

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class Settings(BaseSettings):
    debug: bool = False
    secret_key: str
    environment: str
    app_name: str = "Joby API"

    allowed_hosts: list
    https_only: bool = True

    # database credential
    db_url: str
    db_multi_thread: bool = False

    model_config = SettingsConfigDict(env_file=os.path.join(ROOT_DIR, "env", ".env"), extra='ignore')


SETTINGS = Settings()
# @lru_cache()
# def get_settings():
#     return Settings()
