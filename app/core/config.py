from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', case_sensitive=True)

    DATABASE_URL: Optional[str] = None
    KAFKA_URL: Optional[str] = None

    API_KEY: str = "d85f995853025e164836e41ebb0b74150e4ac46f3f2536ac0c3b69272ea4371f"
    SECRET_KEY: str = "29158654245401a5a12c9a64bf2c00301ef3616f11b73d61f94af3c66f854400"

    # testnet url
    BASE_URL_TESTNET: str = "https://testnet.binancefuture.com" 

    # mainnet url
    BASE_URL_MAINNET: str = "https://fapi.binancefuture.com"

settings = Settings()