from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', case_sensitive=True)

    IS_TESTNET: bool = True

    API_KEY: str = "d85f995853025e164836e41ebb0b74150e4ac46f3f2536ac0c3b69272ea4371f"
    SECRET_KEY: str = "29158654245401a5a12c9a64bf2c00301ef3616f11b73d61f94af3c66f854400"

    # TESTNET URL
    BASE_URL_TESTNET: str = "https://testnet.binancefuture.com"
    WS_URL_TESTNET: str = "wss://fstream.binancefuture.com/ws"

    # MAINNET URL
    BASE_URL_MAINNET: str = "https://fapi.binancefuture.com"
    WS_URL_MAINNET: str = "wss://fstream.binance.com/ws"

    # ACCOUNT EXCHANGE URL
    BASE_URL_ACCOUNT_EXCHANGE: str = "https://testnet.binancefuture.com/api/v1"
    ACCOUNT_ID: str = "BINANCE-MAIN-TRUNGANH-1"

    KAFKA_BOOTSTRAP_SERVERS: str = "192.168.110.154:19092"
    KAFKA_TOPIC_1: str = os.getenv("KAFKA_TOPIC_1", "dev.events_order_sync")

    MINUTES_KEEP_ALIVE_LISTEN_KEY: int = 30

settings = Settings()