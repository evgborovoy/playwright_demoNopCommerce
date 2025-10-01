import pytest


@pytest.mark.smoke
class TestProductsSmoke:
    """
    Smoke tests for critical product functionality
    """

    def test_main_categories_accessible(self, products_page):
        categories = [
            "/computers",
            "/electronics",
            "/books",
            "/digital-downloads"
        ]

        for category in categories:
            products_page.navigate(category)
            assert products_page.is_visible(products_page.PRODUCT_ITEMS) or products_page.has_subcategories()
            products_page.logger.info(f"{category} category accessible")

    def test_search_functionality_working(self, products_page):
        products_page.navigate("/books")
        products_page.search_products("book")

        assert products_page.is_visible(products_page.PRODUCT_ITEMS) or products_page.is_visible(".no-result")
        products_page.logger.info("Search functionality working")

    def test_product_details_accessible(self, products_page):
        products_page.navigate("/books")
        product_names = products_page.get_product_names()

        if product_names:
            products_page.click_product(product_names[0])
            assert products_page.is_visible(".product-essential")
            products_page.logger.info("Product details pages accessible")
        else:
            products_page.logger.info("No products available for details test")
