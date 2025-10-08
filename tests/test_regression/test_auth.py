from utils.helpers import generate_random_email


class TestLoginRegression:
    """
    Regression tests for login functionality
    """

    def test_login_page_loading(self, login_page):
        assert login_page.is_login_page_loaded(), "Login page should be properly loaded"
        assert login_page.is_visible(login_page.EMAIL_INPUT), "Email input should be visible"
        assert login_page.is_visible(login_page.PASSWORD_INPUT), "Password input should be visible"
        assert login_page.is_visible(login_page.LOGIN_BUTTON), "Login button should be visible"
        login_page.logger.info("Login page loads correctly with all elements")

    def test_login_with_invalid_credentials(self, login_page, home_page):
        login_page.login("invalid@example.com", "wrongpassword123")
        error_message = login_page.get_error_message()
        assert error_message, "Error message should be displayed for invalid credentials"
        assert "Login was unsuccessful" in error_message, "Error message should indicate login failure"

        home_page.navigate_to_home()
        assert home_page.is_user_logged_out(), "User should not be logged in with invalid credentials"
        login_page.logger.info("Invalid credentials handled correctly")

    def test_login_with_empty_credentials(self, login_page):
        login_page.login("", "")
        assert login_page.is_login_page_loaded(), "Should remain on login page with empty credentials"
        login_page.logger.info("Empty credentials handled correctly")

    def test_remember_me_functionality(self, login_page):
        login_page.click(login_page.REMEMBER_ME_CHECKBOX)
        is_checked = login_page.page.is_checked(login_page.REMEMBER_ME_CHECKBOX)
        assert is_checked, "Remember me checkbox should be checkable"
        login_page.click(login_page.REMEMBER_ME_CHECKBOX)
        login_page.logger.info("Remember me checkbox works correctly")

    def test_forgot_password_link(self, login_page):
        login_page.click_forgot_password()
        login_page.page.wait_for_url("**/passwordrecovery")
        assert "passwordrecovery" in login_page.page.url, "Should be redirected to password recovery page"
        login_page.logger.info("Forgot password link works correctly")

    def test_login_with_random_email(self, login_page, home_page):
        random_email = generate_random_email()
        login_page.login(random_email, "somepassword123")

        error_message = login_page.get_error_message()
        assert error_message, "Should show error for non-existent user"

        home_page.navigate_to_home()
        assert home_page.is_user_logged_out(), "Should not be logged in with random email"
        login_page.logger.info("Random email login correctly fails")


class TestLoginLogoutFlow:
    """
    Regression Tests for complete login and logout flow
    """

    def test_user_login_state_changes(self, home_page, login_page):
        home_page.navigate_to_home()
        assert home_page.is_user_logged_out(), "User should start logged out"
        home_page.logger.info("PASS: Initial state: user logged out")

        home_page.click_login()
        assert login_page.is_login_page_loaded(), "Should be on login page"
        home_page.logger.info("Navigated to login page")

        login_page.login("wrong@example.com", "wrongpass")
        error_message = login_page.get_error_message()
        assert error_message, "Should show login error"

        home_page.navigate_to_home()
        assert home_page.is_user_logged_out(), "User should still be logged out after failed login"
        home_page.logger.info("PASS: User remains logged out after failed login")
