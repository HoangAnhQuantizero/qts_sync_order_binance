from loguru import logger
from app.services.keep_alive_listen_key import keep_alive_listen_key
from app.websocket_client import WebSocketService
from app.core.config import settings
from app.services.create_listen_key import create_listen_key
import threading

if __name__ == "__main__":
    websocket_service = WebSocketService(settings.WS_URL_TESTNET)

    listen_key = None
    listen_key_data = create_listen_key(
        settings.API_KEY, 
        settings.SECRET_KEY, 
        settings.BASE_URL_TESTNET
    )

    if listen_key_data.get("success"):  
        listen_key = listen_key_data.get("listenKey")
        # logger.success(f"Listen key created successfully: {listen_key}")
    else:
        raise Exception(listen_key_data.get("message"))

    websocket_service.listen_key = listen_key

    threading.Thread(target=keep_alive_listen_key, args=(settings.BASE_URL_TESTNET, settings.API_KEY, listen_key)).start()
    
    websocket_service.start()
