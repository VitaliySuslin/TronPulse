from enum import Enum

from app.src.app.config import settings


class BackendServicesNameEnum(str, Enum):
    name = settings.NAME
