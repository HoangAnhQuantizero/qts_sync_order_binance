from loguru import logger
from app.services.create_signature import create_signature
import requests
from app.core.config import settings

def create_listen_key(
    api_key: str, 
    secret_key: str, 
    base_url: str):

    endpoint = "/fapi/v1/listenKey"
    payload = {}
    signature = create_signature(payload, secret_key)

    payload["signature"] = signature

    headers = {"X-MBX-APIKEY": api_key}
    response = requests.post(base_url + endpoint, headers=headers, params=payload)

    if response.status_code != 200:
        return {
            "success": False,
            "message": "Failed to get listenKey"
        }

    return {
        "success": True,
        "listenKey": response.json().get("listenKey")
    }

if __name__ == "__main__":
    print(create_listen_key(
        api_key=settings.API_KEY,
        secret_key=settings.SECRET_KEY,
        base_url=settings.BASE_URL_TESTNET
    ))