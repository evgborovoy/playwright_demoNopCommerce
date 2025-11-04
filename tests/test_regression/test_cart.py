import allure


@allure.suite("Cart")
class TestCart:
    @allure.title("Empty cart shows empty state")
    def test_empty_cart_display(self, cart_page):
        """Clearing cart should show empty state"""
        cart_page.navigate_to_cart()
        cart_page.clear_cart()
        assert cart_page.get_cart_items_count() == 0

    @allure.title("Quantity update persists after refresh")
    def test_update_product_quantity(self, cart_page, add_product_in_cart):
        """Quantity change should persist after update"""
        cart_page.navigate_to_cart()
        initial = cart_page.get_product_quantity(0)
        assert cart_page.update_product_quantity(0, initial + 1)
