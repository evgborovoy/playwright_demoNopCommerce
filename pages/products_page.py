import time
import re
from .base_page import BasePage
from playwright.sync_api import expect


class ProductsPage(BasePage):
    SEARCH_BOX = "#small-searchterms"
    SEARCH_BUTTON = "button[type='submit']"
    PRODUCT_ITEMS = ".product-item"
    PRODUCT_TITLES = ".product-title a"

    CATEGORY_BLOCKS = ".category-grid .item-box"

    ADD_TO_CART_BUTTON = "button.add-to-cart-button"
    BAR_NOTIFICATION = ".bar-notification"
    BAR_NOTIFICATION_SUCCESS = ".bar-notification.success"
    CART_QUANTITY = ".cart-qty"
    AJAX_LOADING = ".ajax-loading-block"

    def navigate_to_computers(self):
        self.navigate("/computers")
        self.wait_for_category_page()

    def wait_for_category_page(self):
        self.page.wait_for_selector(f"{self.CATEGORY_BLOCKS}, {self.PRODUCT_ITEMS}",
                                    state="visible", timeout=10000)
        self.logger.info("Category page loaded")

    def has_subcategories(self) -> bool:
        return self.page.locator(self.CATEGORY_BLOCKS).count() > 0

    def get_subcategory_names(self) -> list:
        names = []
        for category in self.page.locator(self.CATEGORY_BLOCKS).all():
            title = category.locator("h2 a").text_content()
            if title:
                names.append(title.strip())
        return names

    def wait_for_products(self):
        self.page.wait_for_selector(self.PRODUCT_ITEMS, state="visible", timeout=10000)
        self.logger.info("Products loaded")

    def click_subcategory(self, subcategory_name: str):
        self.logger.info(f"Clicking subcategory: {subcategory_name}")
        subcategory_link = self.page.locator(f"h2 a:has-text('{subcategory_name}')").first
        subcategory_link.click()
        self.wait_for_products()

    def navigate_to_desktops(self):
        self.navigate_to_computers()
        if self.has_subcategories():
            self.click_subcategory("Desktops")

    def navigate_to_notebooks(self):
        self.navigate_to_computers()
        if self.has_subcategories():
            self.click_subcategory("Notebooks")

    def search_products(self, search_term: str):
        self.logger.info(f"Searching for: {search_term}")
        self.fill(self.SEARCH_BOX, search_term)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_products()

    def get_products_count(self) -> int:
        return self.page.locator(self.PRODUCT_ITEMS).count()

    def get_product_names(self) -> list:
        names = []
        for product in self.page.locator(self.PRODUCT_TITLES).all():
            name = product.text_content()
            if name:
                names.append(name.strip())
        return names

    def wait_for_product_details(self):
        self.page.wait_for_selector(".product-essential", state="visible", timeout=10000)
        self.logger.info("Product details page loaded")

    def click_product(self, product_name: str):
        self.logger.info(f"Clicking product: {product_name}")
        product_link = self.page.locator(f"a:has-text('{product_name}')").first
        product_link.click()
        self.wait_for_product_details()

    def can_add_to_cart(self) -> bool:
        return (self.page.is_visible(self.ADD_TO_CART_BUTTON) and
                self.page.locator(self.ADD_TO_CART_BUTTON).first.is_enabled())

    def get_cart_quantity(self) -> int:
        try:
            cart_text = self.page.locator(self.CART_QUANTITY).text_content()
            if cart_text:
                numbers = re.findall(r'\d+', cart_text)
                return int(numbers[0]) if numbers else 0
        except:
            pass
        return 0

    def wait_for_page_stability(self, timeout=3000):
        try:
            # wait for any ongoing animations to complete
            self.logger.info("Wait page stability")
            self.page.wait_for_load_state('networkidle', timeout=timeout)

            # wait for any loading indicators to disappear
            loading_indicator = self.page.locator(self.AJAX_LOADING)
            if loading_indicator.is_visible():
                expect(loading_indicator).to_be_hidden(timeout=2000)

        except:
            # if networkidle times out, just continue
            pass

    def wait_for_button_ready(self):
        add_button = self.page.locator(self.ADD_TO_CART_BUTTON).first
        expect(add_button).to_be_visible(timeout=5000)
        expect(add_button).to_be_enabled(timeout=5000)
        add_button.scroll_into_view_if_needed()
        self.wait_for_page_stability()

    def wait_for_cart_notification(self, timeout=10000):
        start_time = time.time()

        while time.time() - start_time < timeout / 1000:
            try:
                success_notification = self.page.locator(self.BAR_NOTIFICATION_SUCCESS)
                if success_notification.is_visible():
                    self.logger.info("Success notification appeared")
                    return True
            except:
                pass

            try:
                current_quantity = self.get_cart_quantity()
                if current_quantity > 0:
                    self.logger.info(f"Cart quantity updated to {current_quantity}")
                    return True
            except:
                pass
        return False

    def add_to_cart(self):
        self.logger.info("Attempting to add product to cart")
        if not self.can_add_to_cart():
            self.logger.info("Product cannot be added to cart")
            return False

        try:
            self.wait_for_button_ready()
            initial_quantity = self.get_cart_quantity()
            add_button = self.page.locator(self.ADD_TO_CART_BUTTON).first
            add_button.click()
            success = self.wait_for_cart_notification(15000)

            if success:
                self.logger.info("Product added to cart successfully")
                return True
            else:
                final_quantity = self.get_cart_quantity()
                if final_quantity > initial_quantity:
                    self.logger.info(f"Cart quantity increased from {initial_quantity} to {final_quantity}")
                    return True

                self.logger.error("Could not verify product was added to cart")
                return False

        except Exception as e:
            self.logger.error(f"Error adding to cart: {e}")
            return False
