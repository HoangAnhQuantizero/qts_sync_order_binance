import json
import websocket
from loguru import logger
from app.handlers.base_handler import BaseHandler

class WebSocketService:
    def __init__(self, url: str):
        self.url = url
        self.ws = None
        self.listen_key = None
        self.message_handler = BaseHandler()

    def on_open(self, ws):
        logger.success("WebSocket connection opened")

    def on_message(self, ws, message: str):
        try:
            data = json.loads(message)
            self.message_handler.handle_message(data)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def on_error(self, ws, error):
        logger.error(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logger.info(f"WebSocket closed: {close_status_code}, {close_msg}")

    def ping(self):
        self.ws.send("ping")

    def start(self):
        websocket_url = f"{self.url}/{self.listen_key}"
        logger.info(f"WebSocket URL: {websocket_url}")
        self.ws = websocket.WebSocketApp(
            websocket_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

        self.ws.run_forever()

    def stop_service(self):
        self.ws.close()
