import requests
from typing import Optional, Dict
from pydantic import BaseModel


class TronClient:
    def __init__(self, network: str = "mainnet"):
        self.network = network
        self.base_url = self._get_base_url(network)

    def _get_base_url(self, network: str) -> str:
        networks = {
            "mainnet": "https://api.trongrid.io",
            "shasta": "https://api.shasta.trongrid.io",
            "nile": "https://nile.trongrid.io"
        }
        return networks.get(network, networks["mainnet"])

    def get_wallet_info(self, address: str) -> Optional[Dict]:
        try:
            url = f"{self.base_url}/v1/accounts/{address}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # For debug
            # print("API Response:", data)

            if not data.get("data"):
                return None

            account = data["data"][0]
            bandwidth = account.get("free_net_usage", None)
            energy = account.get("account_resource", {}).get("energy_usage", None)
            trx_balance = account.get("balance", 0) / 1_000_000  # TRX в формате SUN
            trc20_balances = account.get("trc20", [])

            return {
                "address": account.get("address"),
                "bandwidth": bandwidth,
                "energy": energy,
                "trx_balance": trx_balance,
                "trc20_balances": trc20_balances
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error while requesting Tron API: {str(e)}")
