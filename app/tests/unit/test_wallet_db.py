import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.app.db.orm.wallet import WalletRequest
from app.src.app.extensions.sqlalchemy import PoolConnector


@pytest.mark.asyncio
async def test_wallet_request_insert():
    test_address = "TPAZM1hkbGWrtruhYFfSD9KNLyG5nK7uyu"
    test_bandwidth = 5000
    test_energy = 1000
    test_trx_balance = 0.049697

    wallet_request = WalletRequest(
        address=test_address,
        bandwidth=test_bandwidth,
        energy=test_energy,
        trx_balance=test_trx_balance,
    )

    session: AsyncSession = await PoolConnector.get_session().__anext__()

    session.add(wallet_request)
    await session.commit()

    result = await session.execute(select(WalletRequest).where(WalletRequest.address == test_address))
    saved_wallet = result.scalars().first()

    assert saved_wallet is not None
    assert saved_wallet.address == test_address
    assert saved_wallet.bandwidth == test_bandwidth
    assert saved_wallet.energy == test_energy
    assert saved_wallet.trx_balance == test_trx_balance

    await session.delete(saved_wallet)
    await session.commit()
