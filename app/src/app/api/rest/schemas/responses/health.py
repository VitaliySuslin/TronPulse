from typing import Optional

from pydantic import BaseModel

from src.app.enums.tools import HealthStatusType


class HealthSchema(BaseModel):
    status: HealthStatusType = HealthStatusType.ok
    sql_status: Optional[HealthStatusType] = HealthStatusType.error
