from enum import Enum

from src.app.config import settings


class BackendServicesNameEnum(str, Enum):
    name = settings.NAME
