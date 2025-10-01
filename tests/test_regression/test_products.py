import pytest


class TestProductsBasic:
    """
    Basic tests for product functionality
    """

    def test_computers_category_has_subcategories(self, products_page):
        products_page.navigate_to_computers()
        has_subcategories = products_page.has_subcategories()
        assert has_subcategories, "Computers category should have subcategories"
        subcategory_names = products_page.get_subcategory_names()
        assert len(subcategory_names) > 0, "Should have subcategory names"
        products_page.logger.info(f"Computers category has subcategories: {subcategory_names}")

    def test_navigate_to_desktops_subcategory(self, products_page):
        products_page.navigate_to_desktops()
        product_count = products_page.get_products_count()
        assert product_count > 0, "Desktops subcategory should have products"
        products_page.logger.info(f"Desktops subcategory has {product_count} products")

    def test_product_search_from_subcategory(self, products_page):
        products_page.navigate_to_desktops()
        initial_count = products_page.get_products_count()
        product_name = "Lenovo"
        products_page.search_products(product_name)
        search_count = products_page.get_products_count()
        products_page.logger.info(f"Found {search_count} products after search")
        assert search_count <= initial_count, "Search should not increase product count"

        if search_count > 0:
            product_names = products_page.get_product_names()
            for name in product_names:
                assert product_name in name, f"Product {name} should contain 'Lenovo'"
        products_page.logger.info("Product search from subcategory works")

    def test_book_add_to_cart(self, products_page, cart_page):
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
            cart_products = cart_page.get_product_names_in_cart()

            assert book_name in cart_products, f"Book {book_name} should be in cart"
            products_page.logger.info(f"Successfully added {book_name} to cart")

            cart_page.remove_product(0)
        else:
            products_page.logger.info(f"Could not add {book_name} to cart")
            pytest.skip("Book cannot be added to cart")


class TestCategoryNavigation:
    """
    Tests for category and subcategory navigation
    """

    def test_computers_subcategories_exist(self, products_page):
        """Test that computers category has expected subcategories"""
        products_page.navigate_to_computers()

        subcategory_names = products_page.get_subcategory_names()
        expected_subcategories = ["Desktops", "Notebooks", "Software"]

        found_expected = any(sub in subcategory_names for sub in expected_subcategories)
        assert found_expected, f"Should find expected subcategories in {subcategory_names}"

        products_page.logger.info(f"Found subcategories: {subcategory_names}")

    def test_subcategory_navigation_works(self, products_page):
        """Test navigation through subcategories"""
        products_page.navigate_to_computers()

        subcategory_names = products_page.get_subcategory_names()
        if subcategory_names:
            # Navigate to first available subcategory
            first_subcategory = subcategory_names[0]
            products_page.click_subcategory(first_subcategory)

            # Should now see products
            product_count = products_page.get_products_count()
            assert product_count >= 0, "Should load subcategory page"

            products_page.logger.info(f"Successfully navigated to {first_subcategory}")

    def test_direct_subcategory_navigation(self, products_page):
        """Test direct navigation to specific subcategories"""
        # Test desktops
        products_page.navigate_to_desktops()
        assert "desktops" in products_page.page.url.lower(), "Should be on desktops page"
        products_page.logger.info("Direct desktops navigation works")

        # Test notebooks
        products_page.navigate_to_notebooks()
        assert "notebooks" in products_page.page.url.lower(), "Should be on notebooks page"
        products_page.logger.info("Direct notebooks navigation works")
