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

    try:
        while True: 
            response = requests.put(url, headers=headers, params=params)
            
            if response.status_code != 200:
                logger.error(f"Failed to keep alive listen key: {response.json()}")
                continue
            elif response.status_code == 200:
                logger.success(f"Keep alive listen key: {response.json()}")
            else:
                logger.error(f"Failed to keep alive listen key: {response.json()}")
                continue

            time.sleep(settings.MINUTES_KEEP_ALIVE_LISTEN_KEY * 60)

    except Exception as e:
        logger.error(f"Failed to keep alive listen key: {e}")

if __name__ == "__main__":
    print(keep_alive_listen_key(
        url="https://testnet.binancefuture.com", 
        api_key="d85f995853025e164836e41ebb0b74150e4ac46f3f2536ac0c3b69272ea4371f",
        listen_key="6rFENRhWBfLfRofCoLHOyJyyjblhYq64En4gyamwgBir5NEVXVVCUAhKn6v1MQO7")
        )