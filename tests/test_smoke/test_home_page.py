import pytest


@pytest.mark.smoke
class TestHomePage:
    """
    Smoke tests for nopCommerce home page
    """

    def test_home_page_loading(self, home_page):
        home_page.navigate_to_home()

        title = home_page.get_page_title()
        home_page.logger.info(f"Page title: {title}")

        assert "nopCommerce" in title
        home_page.logger.info("Home page loaded successfully with correct title")

    def test_login_link_visible(self, home_page):
        home_page.navigate_to_home()

        is_visible = home_page.is_login_link_visible()
        home_page.logger.info(f"Login link visible: {is_visible}")

        assert is_visible, "Login link should be visible on home page"
        home_page.logger.info("Login link is visible as expected")

    def test_register_link_visible(self, home_page):
        home_page.navigate_to_home()

        is_visible = home_page.is_register_link_visible()
        home_page.logger.info(f"Register link visible: {is_visible}")

        assert is_visible, "Register link should be visible on home page"
        home_page.logger.info("Register link is visible as expected")
