from pydantic import BaseModel, Field
from typing import Optional


class PaginationRequest(BaseModel):
    page: int = Field(default=1, ge=1, description="Номер страницы")
    size: int = Field(default=10, ge=1, le=100, description="Количество элементов на странице")



class WalletInfoRequest(BaseModel):
    address: str = Field(..., description="Адрес кошелька Tron")
    network: Optional[str] = Field(default="mainnet", description="Сеть Tron (mainnet, shasta, nile)")
