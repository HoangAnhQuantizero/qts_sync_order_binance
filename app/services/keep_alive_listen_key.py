from loguru import logger
import requests
from app.core.config import settings
import time

def keep_alive_listen_key(url: str, api_key: str, listen_key: str):
    url = f"{url}/fapi/v1/listenKey"
    headers = {"X-MBX-APIKEY": api_key}

    params = {
        "listenKey": listen_key
    }

    while True: 
        time.sleep(settings.MINUTES_KEEP_ALIVE_LISTEN_KEY * 60)
        response = requests.put(url, headers=headers, params=params)
        logger.info(f"Keep alive listen key: {response.json()}")

if __name__ == "__main__":
    print(keep_alive_listen_key(
        url="https://testnet.binancefuture.com", 
        api_key="d85f995853025e164836e41ebb0b74150e4ac46f3f2536ac0c3b69272ea4371f",
        listen_key="6rFENRhWBfLfRofCoLHOyJyyjblhYq64En4gyamwgBir5NEVXVVCUAhKn6v1MQO7")
        )