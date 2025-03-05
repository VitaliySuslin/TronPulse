import logging
import os
from typing import List, Union, Type
from dotenv import load_dotenv

from pydantic_settings import BaseSettings


load_dotenv()

class Settings(BaseSettings):
    """Base class of settings"""

    DEBUG: bool
    RELOAD: bool
    NAME: str = 'TronPulse'
    LOG_LEVEL: int = logging.WARNING
    USE_JSON_LOG_FORMAT: bool = False
    API_PATH_PREF: str = '/api/v1'
    APP_HOST: str
    APP_PORT: int = 8080
    CORS_ORIGINS: List[str] = ['*']
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_ECHO: bool = False

    class Config:
        env_file_encoding: str = 'utf-8'


class LocalSettings(Settings):
    """Local settings"""

    DEBUG: bool = True
    RELOAD: bool = True
    APP_HOST: str = '0.0.0.0'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = '020290'
    POSTGRES_DB: str = 'tron_pulse'
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432


class ProdSettings(Settings):
    """Prod settings"""

    DEBUG: bool = False
    RELOAD: bool = False
    APP_HOST: str = ''
    POSTGRES_USER: str = ''
    POSTGRES_PASSWORD: str = ''
    POSTGRES_DB: str = ''
    POSTGRES_HOST: str = ''
    POSTGRES_PORT: int = 0


def get_settings() -> Union[ProdSettings, LocalSettings]:
    env_type: str = os.environ.get('__ENV__', 'local')
    config_cls_dict: dict[str, Type[Union[ProdSettings, LocalSettings]]] = {
        'prod': ProdSettings,
        'local': LocalSettings,
    }
    return config_cls_dict.get(env_type, LocalSettings)()


settings: Union[ProdSettings, LocalSettings] = get_settings()
