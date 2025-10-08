import allure
from playwright.sync_api import Page
from utils.logger import logger
from config.settings import Config
from config.test_data import TestData


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logger
        self.base_url = Config.BASE_URL.rstrip('/')
        self.test_data = TestData

    @allure.step("Navigate to {path}")
    def navigate(self, path: str = ""):
        if path.startswith('http'):
            url = path
        else:
            url = path if path.startswith('/') else f"/{path}"

        self.logger.info(f"Navigating to: {url}")

        try:
            self.page.goto(url)
            self.logger.info("Navigation successful")
        except Exception as e:
            self.logger.error(f"Navigation failed: {e}")
            raise

    @allure.step("Click on {selector}")
    def click(self, selector: str):
        self.logger.info(f"Clicking: {selector}")
        self.page.locator(selector).first.click(timeout=Config.DEFAULT_TIMEOUT)

    @allure.step("Fill {selector} with {text}")
    def fill(self, selector: str, text: str):
        self.logger.info(f"Filling {selector} with: {text}")
        self.page.locator(selector).first.fill(text)

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).first.text_content(timeout=Config.DEFAULT_TIMEOUT) or ""

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).first.is_visible(timeout=Config.DEFAULT_TIMEOUT)

    @allure.step("Wait for selector {selector}")
    def wait_for_selector(self, selector: str, timeout: int = Config.DEFAULT_TIMEOUT):
        """Wait for selector to be visible, using centralized timeout"""
        self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)
