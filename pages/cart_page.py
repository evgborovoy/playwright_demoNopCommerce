from playwright.sync_api import expect

from .base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS = ".cart tbody tr"
    PRODUCT_NAMES = ".product a"
    QUANTITY_INPUTS = ".qty-input"
    UNIT_PRICES = ".product-unit-price"
    SUBTOTALS = ".product-subtotal"
    REMOVE_BUTTONS = ".remove-btn"
    EMPTY_CART_MESSAGE = ".order-summary-content"
    TERMS_CHECKBOX = "#termsofservice"
    CHECKOUT_BUTTON = "#checkout"
    CART_TOTAL = ".order-total .product-price"

    def navigate_to_cart(self):
        self.navigate("cart")
        self.wait_for_cart_loaded()

    def wait_for_cart_loaded(self):
        self.logger.info("Waiting for cart to load")

        try:
            self.page.wait_for_selector(f"{self.CART_ITEMS}, {self.EMPTY_CART_MESSAGE}",
                                        state="visible", timeout=15000)
            self.logger.info("Cart loaded")
        except Exception as e:
            self.logger.warning(f"Cart loading warning: {e}")

    def get_cart_items_count(self) -> int:
        try:
            items = self.page.locator(self.CART_ITEMS).filter(
                has=self.page.locator(".product-name")
            )
            count = items.count()
            self.logger.info(f"Cart has {count} items")
            return count
        except Exception as e:
            self.logger.warning(f"Error counting cart items: {e}")
            return 0

    def get_product_quantity(self, item_index: int = 0):
        qty_inputs = self.page.locator(self.QUANTITY_INPUTS)
        expect(qty_inputs.nth(item_index)).to_be_visible(timeout=5000)
        val = qty_inputs.nth(item_index).input_value()
        try:
            return int(val)
        except (ValueError, TypeError):
            self.logger.warning(f"Cannot parse quantity value '{val}', returning 0")
            return 0


    def is_cart_empty(self) -> bool:
        if self.get_cart_items_count() == 0:
            return True

        if self.is_visible(self.EMPTY_CART_MESSAGE):
            message = self.get_text(self.EMPTY_CART_MESSAGE)
            return "empty" in message.lower() if message else False

        return False

    def get_product_names(self) -> list:
        names = []
        try:
            for name_element in self.page.locator(self.PRODUCT_NAMES).all():
                name = name_element.text_content()
                if name and name.strip():
                    names.append(name.strip())
        except Exception as e:
            self.logger.warning(f"Error getting product names: {e}")
        return names

    def update_product_quantity(self, product_index: int, new_quantity: int):
        self.logger.info(f"Updating product {product_index + 1} quantity to {new_quantity}")

        try:
            quantity_inputs = self.page.locator(self.QUANTITY_INPUTS)
            if quantity_inputs.count() > product_index:
                quantity_inputs.nth(product_index).fill(str(new_quantity))
                self.page.press(self.QUANTITY_INPUTS, "Enter")
                self.wait_for_cart_loaded()
                return True
        except Exception as e:
            self.logger.error(f"Error updating quantity: {e}")
        return False

    def remove_product(self, product_index: int = 0):
        self.logger.info(f"Removing product {product_index + 1} from cart")

        try:
            remove_buttons = self.page.locator(self.REMOVE_BUTTONS)
            if remove_buttons.count() > product_index:
                remove_buttons.nth(product_index).click()
                self.wait_for_cart_loaded()
                return True
        except Exception as e:
            self.logger.error(f"Error removing product: {e}")
        return False

    def clear_cart(self):
        self.logger.info("Start clear cart")
        while not self.is_cart_empty():
            self.remove_product(0)
