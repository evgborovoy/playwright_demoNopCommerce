import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL: str = os.getenv("BASE_URL", "https://demo.nopcommerce.com")
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    DEFAULT_TIMEOUT: int = 15000
    USER_AGENT: str = os.getenv("PW_USER_AGENT")