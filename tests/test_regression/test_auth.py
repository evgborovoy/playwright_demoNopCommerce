import allure


class TestLoginRegression:
    @allure.title("Login page presents the form")
    def test_login_page_loading(self, login_page):
        """Open login page before asserting presence"""
        login_page.navigate_to_login()
        assert login_page.is_login_page_loaded(), "Login page should be properly loaded"

    @allure.title("Invalid credentials show server-side error")
    def test_login_with_invalid_credentials(self, login_page, home_page):
        login_page.navigate_to_login()
        login_page.login("invalid@example.com", "wrongpassword123")
        msg = login_page.get_error_message()
        assert msg and "Login was unsuccessful" in msg

    @allure.title("'Remember me' checkbox can be toggled")
    def test_remember_me_functionality(self, login_page):
        login_page.navigate_to_login()
        login_page.click(login_page.REMEMBER_ME_CHECKBOX)

    @allure.title("'Forgot password' link opens recovery")
    def test_forgot_password_link(self, login_page):
        login_page.navigate_to_login()
        login_page.click_forgot_password()
