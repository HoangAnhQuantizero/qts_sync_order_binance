from loguru import logger
from app.services.get_account_exchange_api_key import get_account_exchange_api_keys
from app.services.keep_alive_listen_key import keep_alive_listen_key
from app.websocket_client import WebSocketService
from app.core.config import settings
from app.services.create_listen_key import create_listen_key
import threading
import signal
import sys

def signal_handler(signum, frame):
    """Xử lý signal Ctrl+C"""
    logger.info(f"Received signal {signum}, shutting down...")
    sys.exit(0)

if __name__ == "__main__":
    # Đăng ký signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    websocket_service = WebSocketService(settings.WS_URL_TESTNET)
    keep_alive_thread = None

    try:
        listen_key = None
        url = None
        API_KEY = None
        SECRET_KEY = None

        if settings.IS_TESTNET:
            url = settings.BASE_URL_TESTNET
            API_KEY = settings.API_KEY
            SECRET_KEY = settings.SECRET_KEY
        else:
            account_exchange_data = get_account_exchange_api_keys(
                url=settings.BASE_URL_ACCOUNT_EXCHANGE,
                account_id=settings.ACCOUNT_ID
            )   
            if account_exchange_data.get("success"):
                API_KEY = account_exchange_data.get("data").get("api_key")
                SECRET_KEY = account_exchange_data.get("data").get("secret_key")
            else:
                raise Exception(account_exchange_data.get("message"))

            url = settings.BASE_URL_MAINNET

        listen_key_data = create_listen_key(
            API_KEY, 
            SECRET_KEY, 
            url
        )

        if listen_key_data.get("success"):  
            listen_key = listen_key_data.get("listenKey")
        else:
            raise Exception(listen_key_data.get("message"))

        websocket_service.listen_key = listen_key

        keep_alive_thread = threading.Thread(
            target=keep_alive_listen_key, 
            args=(settings.BASE_URL_TESTNET, settings.API_KEY, listen_key),
            daemon=True
        )
        keep_alive_thread.start()
        
        logger.info("Starting WebSocket service...")
        websocket_service.start()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        logger.info("Shutting down...")
        if keep_alive_thread and keep_alive_thread.is_alive():
            logger.info("Stopping keep alive thread...")
        logger.info("Application stopped")
