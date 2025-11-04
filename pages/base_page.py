import re
import allure
from playwright.sync_api import Page, expect
from utils.logger import logger
from config.settings import Config
from config.test_data import TestData


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logger
        self.base_url = Config.BASE_URL.rstrip("/")
        self.test_data = TestData

    def navigate(self, path: str, wait: str = "domcontentloaded"):
        self.page.goto(path, wait_until=wait)
        self._wait_cloudflare_gate()

    def _wait_cloudflare_gate(self, timeout_ms: int = 12000):
        try:
            title = self.page.title()
        except Exception:
            title = ""
        if "Just a moment" not in title:
            return
        self.logger.warning("[CF] Interstitial detected")
        elapsed = 0
        step = 500
        while elapsed < timeout_ms:
            self.page.wait_for_timeout(step)
            elapsed += step
            try:
                if "Just a moment" not in self.page.title():
                    self.logger.info("[CF] Interstitial passed")
                    return
            except Exception:
                pass
        self.logger.warning("[CF] Reloading once…")
        self.page.reload(wait_until="domcontentloaded")
        self.page.wait_for_timeout(1500)

    @allure.step("Click: {selector}")
    def click(self, selector: str):
        """Click the first matching node for a given selector"""
        self.logger.info(f"[CLICK] {selector}")
        self.page.locator(selector).first.click()

    @allure.step("Fill: {selector} -> {text}")
    def fill(self, selector: str, text: str):
        """Fill an input with a given text"""
        self.logger.info(f"[FILL] {selector} -> {text}")
        self.page.locator(selector).first.fill(text)

    def get_text(self, selector: str) -> str:
        """Return text content or empty string if missing"""
        return self.page.locator(selector).first.text_content() or ""

    def is_visible(self, selector: str) -> bool:
        """Synchronous visibility check for quick boolean flows"""
        return self.page.locator(selector).first.is_visible()

    # Web-first assertions (preferred way to reduce flakiness)
    @allure.step("Expect visible: {selector}")
    def expect_visible(self, selector: str):
        """Assert that an element becomes visible"""
        expect(self.page.locator(selector).first).to_be_visible()

    @allure.step("Expect title contains: {text}")
    def expect_title_contains(self, text: str | re.Pattern):
        """Title assertion that waits"""
        if isinstance(text, str):
            pattern = re.compile(re.escape(text), re.IGNORECASE)
            expect(self.page).to_have_title(pattern)
        else:
            expect(self.page).to_have_title(text)
