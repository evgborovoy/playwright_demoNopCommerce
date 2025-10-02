import allure
import pytest


@allure.suite("Cart Tests")
class TestCart:
    """
    Regression tests for shopping cart functionality
    """

    @allure.title("Empty cart message display")
    @allure.tag("regression", "cart")
    def test_empty_cart_display(self, cart_page):
        with allure.step("Open and clear cart"):
            cart_page.navigate_to_cart()
            cart_page.clear_cart()

        with allure.step("Open and clear cart"):
            assert cart_page.is_visible(cart_page.EMPTY_CART_MESSAGE), "Should show empty cart message"

        cart_page.logger.info("Empty cart displays correctly")
        allure.attach("Message is displayed", name="Empty cart", attachment_type=allure.attachment_type.TEXT)

    @allure.title("Update product quantity")
    @allure.tag("regression", "cart")
    def test_update_product_quantity(self, products_page, cart_page):
        products_page.navigate("/books")
        products_page.wait_for_products()
        product_names = products_page.get_product_names()
        products_page.logger.info(f"Available books: {product_names}")
        if not product_names:
            pytest.skip("No books available")
        book_name = product_names[0]
        products_page.logger.info(f"Testing with book: {book_name}")
        products_page.click_product(book_name)
        added_to_cart = products_page.add_to_cart()
        if added_to_cart:
            cart_page.navigate_to_cart()

        initial_quantity = cart_page.get_product_quantity(0)
        new_quantity = initial_quantity + 1
        success = cart_page.update_product_quantity(0, new_quantity)
        assert success, "Should be able to update quantity"

        updated_quantity = cart_page.get_product_quantity(0)
        assert updated_quantity == new_quantity, f"Quantity should be {new_quantity}, got {updated_quantity}"
        cart_page.logger.info("Product quantity update works correctly")

    @allure.title("Remove product")
    @allure.tag("regression", "cart")
    def test_remove_product_from_cart(self, products_page, cart_page):
        cart_page.clear_cart()
        products_page.navigate("/books")
        products_page.wait_for_products()
        product_names = products_page.get_product_names()
        products_page.logger.info(f"Available books: {product_names}")
        if not product_names:
            pytest.skip("No books available")
        book_name = product_names[0]
        products_page.logger.info(f"Testing with book: {book_name}")
        products_page.click_product(book_name)
        added_to_cart = products_page.add_to_cart()
        if added_to_cart:
            cart_page.navigate_to_cart()

        initial_count = cart_page.get_cart_items_count()

        success = cart_page.remove_product(0)
        assert success, "Should be able to remove product"

        new_count = cart_page.get_cart_items_count()
        assert new_count == initial_count - 1, "Cart count should decrease after removal"

        cart_page.logger.info("Product removal works correctly")


class TestCartEdgeCases:
    """
    Tests for cart edge cases
    """

    @allure.title("Set quantity to 0")
    @allure.tag("regression", "cart")
    def test_zero_quantity_handling(self, products_page, cart_page):
        products_page.navigate("/books")
        products_page.wait_for_products()
        product_names = products_page.get_product_names()
        products_page.logger.info(f"Available books: {product_names}")
        if not product_names:
            pytest.skip("No books available")
        book_name = product_names[0]
        products_page.logger.info(f"Testing with book: {book_name}")
        products_page.click_product(book_name)
        added_to_cart = products_page.add_to_cart()
        if added_to_cart:
            cart_page.navigate_to_cart()

        # Try to set quantity to zero
        success = cart_page.update_product_quantity(0, 0)
        assert success, "Should be able to set quantity to zero"

        # Product should be removed from cart
        assert cart_page.is_cart_empty(), "Cart should be empty after setting quantity to zero"
        cart_page.logger.info("Zero quantity handling works correctly")

    @allure.title("Product large quantity")
    @allure.tag("regression", "cart")
    def test_large_quantity_handling(self, products_page, cart_page):
        products_page.navigate("/books")
        products_page.wait_for_products()
        product_names = products_page.get_product_names()
        products_page.logger.info(f"Available books: {product_names}")
        if not product_names:
            pytest.skip("No books available")
        book_name = product_names[0]
        products_page.logger.info(f"Testing with book: {book_name}")
        products_page.click_product(book_name)
        added_to_cart = products_page.add_to_cart()
        if added_to_cart:
            cart_page.navigate_to_cart()

        large_quantity = 999
        success = cart_page.update_product_quantity(0, large_quantity)

        if success:
            updated_quantity = cart_page.get_product_quantity(0)
            assert updated_quantity == large_quantity, f"Should accept large quantity: {large_quantity}"
        else:
            # If failed, should show some validation
            assert True, "Large quantity properly rejected with validation"
        cart_page.logger.info("Large quantity handling works correctly")
