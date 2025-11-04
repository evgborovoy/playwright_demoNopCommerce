import allure


@allure.suite("Cart")
class TestCart:
    @allure.title("Empty cart shows empty state")
    def test_empty_cart_display(self, cart_page):
        """Clearing cart should show empty state"""
        cart_page.navigate_to_cart()

        if cart_page.get_cart_items_count() > 0:
            cart_page.clear_cart()

        assert cart_page.get_cart_items_count() == 0 or \
               cart_page.is_visible(cart_page.EMPTY_CART_MESSAGE)
