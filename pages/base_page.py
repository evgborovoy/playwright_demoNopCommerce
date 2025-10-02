import allure
from playwright.sync_api import Page
from utils.logger import logger
from config.settings import Config


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logger
        self.base_url = Config.BASE_URL.rstrip('/')

    @allure.step("Navigate to {path}")
    def navigate(self, path: str = ""):
        if path.startswith('http'):
            url = path
        elif path:
            url = f"{self.base_url}/{path.lstrip('/')}"
        else:
            url = self.base_url

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
        self.page.locator(selector).first.click()

    @allure.step("Fill {selector} with {text}")
    def fill(self, selector: str, text: str):
        self.logger.info(f"Filling {selector} with: {text}")
        self.page.locator(selector).first.fill(text)

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).first.text_content() or ""

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).first.is_visible()

    def wait_for_selector(self, selector: str, timeout: int = 30000):
        """Wait for selector to be visible"""
        self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)
