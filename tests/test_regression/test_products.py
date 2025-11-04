import allure


@allure.suite("Products")
class TestProductsBasic:
    @allure.title("Computers category shows subcategories")
    def test_computers_category_has_subcategories(self, products_page):
        """Category page should display subcategory grid"""
        products_page.navigate_to_computers()
        assert len(products_page.get_subcategory_names()) > 0

    @allure.title("Notebooks subcategory renders product list")
    def test_navigate_to_desktops_subcategory(self, products_page):
        """We can enter Notebooks and see product list"""
        products_page.navigate_to_computers()
        products_page.navigate_to_notebooks()
        products_page.wait_for_products()
        assert products_page.get_first_product_name()

    @allure.title("Add first desktop to cart shows item in cart")
    def test_add_product_to_cart(self, products_page, cart_page):
        """Add product flow results in an item visible in cart"""
        products_page.navigate_to_computers()
        products_page.navigate_to_software()
        name = products_page.get_first_product_name()
        products_page.add_product_to_cart(name)

        cart_page.navigate_to_cart()
        assert cart_page.get_cart_items_count() >= 1
