import allure

class TestCartSmoke:
    """
    Smoke tests for cart critical functionality
    """

    @allure.title("Loading cart")
    @allure.tag("smoke", "cart")
    def test_cart_page_loading(self, cart_page):
        cart_page.navigate_to_cart()
        assert cart_page.is_visible(cart_page.CART_ITEMS) or cart_page.is_visible(cart_page.EMPTY_CART_MESSAGE)
        cart_page.logger.info("Cart page loads correctly")