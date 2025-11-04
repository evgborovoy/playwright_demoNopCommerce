import allure

@allure.suite("Smoke")
class TestAuthSmoke:
    def test_login_page_accessible(self, login_page):
        login_page.navigate_to_login()
        assert login_page.is_login_page_loaded()

    def test_home_page_login_state_indicators(self, home_page):
        home_page.navigate_to_home()
        assert home_page.is_login_link_visible()

    def test_user_can_navigate_to_login_from_home(self, home_page, login_page):
        home_page.navigate_to_home()
        home_page.click_login()
        assert login_page.is_login_page_loaded()
