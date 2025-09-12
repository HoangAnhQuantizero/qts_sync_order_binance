from loguru import logger
from app.services.keep_alive_listen_key import keep_alive_listen_key
from app.websocket_client import WebSocketService
from app.core.config import settings
from app.services.create_listen_key import create_listen_key
import threading
import signal
import sys
import time

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
        listen_key_data = create_listen_key(
            settings.API_KEY, 
            settings.SECRET_KEY, 
            settings.BASE_URL_TESTNET
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
