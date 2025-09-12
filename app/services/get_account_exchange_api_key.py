import requests
from app.core.config import settings


def get_account_exchange_api_keys(url: str, account_id: str):
    url = f"{url}/accounts/{account_id}/api-keys"
    response = requests.get(url)

    if response.status_code != 200:
        return {
            "success": False,
            "message": response.json()
        }

    data = response.json()

    public_key = None
    for key in data.get("api_keys", []):
        if key.get("type") == "PUBLIC":
            public_key = {
                "api_key": key.get("api_key"),
                "secret_key": key.get("secret")
            }
            break

    if not public_key:
        return {
            "success": False,
            "message": "No PUBLIC api_key found"
        }

    return {
        "success": True,
        "data": public_key
    }

if __name__ == "__main__":
    print(get_account_exchange_api_keys(
        url="http://127.0.0.1:3010/api/v1",
        account_id="BINANCE-MAIN-TRUNGANH-1"
    ))
