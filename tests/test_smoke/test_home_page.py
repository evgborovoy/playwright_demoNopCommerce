import pytest
import allure


@allure.suite("Smoke")
@pytest.mark.smoke
class TestHomePage:
    @allure.title("Home opens and title contains brand")
    def test_home_page_loading(self, home_page):
        """Home opens and title is correct"""
        home_page.navigate_to_home()
        home_page.assert_title()

    @allure.title("Login link is visible to a guest")
    def test_login_link_visible(self, home_page):
        """Login link is visible to a guest"""
        home_page.navigate_to_home()
        assert home_page.is_login_link_visible()

    @allure.title("Register link is visible to a guest")
    def test_register_link_visible(self, home_page):
        """Register link is visible to a guest"""
        home_page.navigate_to_home()
        assert home_page.is_register_link_visible()
