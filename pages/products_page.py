import allure
from playwright.sync_api import expect
from .base_page import BasePage


class ProductsPage(BasePage):
    SEARCH_INPUT = "input[placeholder='Search store']"
    SEARCH_BUTTON = "button[type='submit']"
    PRODUCT_ITEMS = ".product-item"
    PRODUCT_TITLES = ".product-title a"
    CATEGORY_BLOCKS = ".category-grid .item-box"
    ADD_TO_CART_BUTTON = "button.add-to-cart-button"
    BAR_NOTIFICATION = ".bar-notification"
    PRODUCT_LINKS = ".product-title a"

    @allure.step("Search products: {text}")
    def search(self, text: str):
        """Search via header search box"""
        self.fill(self.SEARCH_INPUT, text)
        self.click(self.SEARCH_BUTTON)
        expect(self.page.locator(self.PRODUCT_ITEMS).first).to_be_visible(timeout=10000)

    @allure.step("Get product names on page")
    def get_product_names(self) -> list[str]:
        """Return all product titles on the current listing grid"""
        items = self.page.locator(self.PRODUCT_TITLES)
        count = items.count()
        names: list[str] = []
        for i in range(count):
            name = items.nth(i).text_content() or ""
            name = name.strip()
            if name:
                names.append(name)
        return names

    @allure.step("Check presence of subcategories")
    def has_subcategories(self) -> bool:
        """Some category pages show subcategory tiles instead of product list"""
        return self.page.locator(self.CATEGORY_BLOCKS).count() > 0

    @allure.step("Open 'Computers' category")
    def navigate_to_computers(self):
        """Open Computers and wait until either subcats OR products appear"""
        self.navigate("/computers")
        union = self.page.locator(f"{self.CATEGORY_BLOCKS}, {self.PRODUCT_ITEMS}")
        expect(union.first).to_be_visible(timeout=10000)

    @allure.step("Open 'Notebooks' subcategory")
    def navigate_to_notebooks(self):
        self.page.locator("role=link[name='Notebooks']").first.click()
        expect(self.page.locator(self.PRODUCT_ITEMS).first).to_be_visible(timeout=10000)

    @allure.step("Open 'Software' subcategory")
    def navigate_to_software(self):
        self.page.locator("role=link[name='Software']").first.click()
        expect(self.page.locator(self.PRODUCT_ITEMS).first).to_be_visible(timeout=10000)

    @allure.step("Collect subcategory names")
    def get_subcategory_names(self) -> list[str]:
        names: list[str] = []
        for category in self.page.locator(self.CATEGORY_BLOCKS).all():
            title = category.locator("h2 a").text_content()
            if title:
                names.append(title.strip())
        return names

    @allure.step("Wait for products to be visible")
    def wait_for_products(self):
        """Wait until at least one product is visible"""
        expect(self.page.locator(self.PRODUCT_ITEMS).first).to_be_visible(timeout=10000)

    @allure.step("Read first product name")
    def get_first_product_name(self) -> str:
        self.wait_for_products()
        return (self.page.locator(self.PRODUCT_TITLES).first.text_content() or "").strip()

    @allure.step("Add product to cart: {product_name}")
    def add_product_to_cart(self, product_name: str):
        """Navigate into product details and add to cart"""
        self.page.locator(f"a:has-text('{product_name}')").first.click()
        expect(self.page.locator(".product-essential").first).to_be_visible(timeout=10000)
        self.page.wait_for_load_state("networkidle")
        self.page.locator(self.ADD_TO_CART_BUTTON).first.click()

        toast = self.page.locator(self.BAR_NOTIFICATION).first
        try:
            expect(toast).to_be_visible(timeout=8000)
        except Exception:
            self.logger.info("[ADD TO CART] Toast not detected; proceeding with cart verification later.")
