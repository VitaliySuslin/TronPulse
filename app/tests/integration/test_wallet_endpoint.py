import pytest
from fastapi.testclient import TestClient

from .main import app
from src.app.api.rest.schemas.responses.wallet import WalletInfoResponse


client = TestClient(app)

@pytest.mark.asyncio
async def test_get_wallet_info():
    # test data
    test_address = "TPAZM1hkbGWrtruhYFfSD9KNLyG5nK7uyu"
    test_network = "mainnet"

    response = client.post(
        "/tron/wallet",
        json={"address": test_address, "network": test_network},
    )

    assert response.status_code == 200

    wallet_info = WalletInfoResponse(**response.json())
    assert wallet_info.address == test_address
    assert wallet_info.network == test_network
    assert isinstance(wallet_info.trx_balance, float)
