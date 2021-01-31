from pydantic import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    base_dir: str = os.getcwd()
    media_url: str = os.path.join(base_dir, 'medias')


@lru_cache()
def get_settings():
    return Settings()
