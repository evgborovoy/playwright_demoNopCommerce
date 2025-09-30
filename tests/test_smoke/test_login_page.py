import pytest


@pytest.mark.smoke
class TestAuthSmoke:
    """
    Smoke tests for critical auth functionality
    """

    def test_login_page_accessible(self, login_page):
        login_page.navigate_to_login()
        assert login_page.is_login_page_loaded()
        login_page.logger.info("Login page accessibility - PASSED")

    def test_home_page_login_state_indicators(self, home_page):
        home_page.navigate_to_home()
        assert home_page.is_login_link_visible() or home_page.is_logout_link_visible(), \
            "Should show either login or logout link"
        home_page.logger.info("Home page login state indicators work correctly")

    def test_user_can_navigate_to_login_from_home(self, home_page, login_page):
        home_page.navigate_to_home()
        home_page.click_login()
        assert login_page.is_login_page_loaded(), "Should be redirected to login page"
        login_page.logger.info("Navigation from home to login works correctly")
