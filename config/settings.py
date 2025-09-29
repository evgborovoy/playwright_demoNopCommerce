import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = os.getenv("BASE_URL", "https://demo.nopcommerce.com")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
