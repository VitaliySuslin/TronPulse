from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class WalletResponse(BaseModel):
    id: Optional[int] = Field(default=None, description="ID записи в базе данных")
    address: str = Field(..., description="Адрес кошелька Tron")
    bandwidth: Optional[int] = Field(default=None, description="Оставшаяся пропускная способность")
    energy: Optional[int] = Field(default=None, description="Оставшаяся энергия")
    trx_balance: Optional[float] = Field(default=None, description="Баланс TRX")
    requested_at: Optional[datetime] = Field(default=None, description="Время запроса")

    class Config:
        orm_mode = True

class WalletListResponse(BaseModel):
    items: List[WalletResponse]
    total: int
    page: int
    size: int


class WalletInfoResponse(BaseModel):
    address: str
    bandwidth: Optional[int]
    energy: Optional[int]
    trx_balance: Optional[float]
    network: str

    class Config:
        orm_mode = True
