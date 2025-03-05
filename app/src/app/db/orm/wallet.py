from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime
)
from datetime import datetime

from src.app.extensions.sqlalchemy import Base


class WalletRequest(Base):
    __tablename__ = 'wallet_requests'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False, index=True)
    bandwidth = Column(Integer, nullable=True)
    energy = Column(Integer, nullable=True)
    trx_balance = Column(Float, nullable=True)
    requested_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<WalletRequest(address='{self.address}', bandwidth={self.bandwidth}, " \
               f"energy={self.energy}, trx_balance={self.trx_balance}, requested_at={self.requested_at})>"
