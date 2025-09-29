from playwright.sync_api import Page
from utils.logger import logger


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logger

    def navigate(self, url: str):
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url)

    def click(self, selector: str):
        self.logger.info(f"Clicking on: {selector}")
        self.page.locator(selector).click()

    def fill(self, selector: str, text: str):
        self.logger.info(f"Filling: {selector} with: {text}")
        self.page.locator(selector).fill(text)