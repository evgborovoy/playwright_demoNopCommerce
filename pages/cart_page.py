import allure
from playwright.sync_api import expect
from .base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS = ".cart tbody tr"
    QUANTITY_INPUTS = ".qty-input"
    UPDATE_BUTTON = "button[name='updatecart']"
    REMOVE_BUTTONS = ".remove-btn"
    EMPTY_CART_MESSAGE = ".order-summary-content"

    @allure.step("Open cart page")
    def navigate_to_cart(self):
        """Open the cart page"""
        self.navigate("/cart")

    @allure.step("Clear cart")
    def clear_cart(self):
        """Remove all items from the cart"""
        if self.page.locator(self.CART_ITEMS).count() == 0:
            return
        for btn in self.page.locator(self.REMOVE_BUTTONS).all():
            # Supports both checkbox-like and button-like behavior
            try:
                btn.check()
            except Exception:
                btn.click()
        self.click(self.UPDATE_BUTTON)
        expect(self.page.locator(self.EMPTY_CART_MESSAGE)).to_be_visible()

    @allure.step("Get cart items count")
    def get_cart_items_count(self) -> int:
        """Count meaningful rows by presence of product name cell"""
        return self.page.locator(self.CART_ITEMS).filter(has=self.page.locator(".product-name")).count()

    @allure.step("Read product quantity by index: {item_index}")
    def get_product_quantity(self, item_index: int = 0) -> int:
        """Read quantity input value by index"""
        text = self.page.locator(self.QUANTITY_INPUTS).nth(item_index).input_value()
        try:
            return int(text)
        except Exception:
            return 0

    @allure.step("Set product quantity at index: {item_index} -> {qty}")
    def set_product_quantity(self, item_index: int, qty: int):
        inp = self.page.locator(self.QUANTITY_INPUTS).nth(item_index)
        expect(inp).to_be_attached(timeout=5000)
        inp.fill(str(qty))
        self.page.locator(self.UPDATE_BUTTON).first.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Update product quantity at index {item_index} -> {qty}")
    def update_product_quantity(self, item_index: int, qty: int) -> bool:
        """Update quantity and assert UI reflects the change"""
        locator = self.page.locator(self.QUANTITY_INPUTS).nth(item_index)
        locator.fill(str(qty))
        self.page.wait_for_load_state("networkidle")
        expect(locator).to_have_value(str(qty))
        return True
