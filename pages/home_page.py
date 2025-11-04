import allure
from .base_page import BasePage


class HomePage(BasePage):
    LOGIN_LINK = "role=link[name='Log in']"
    REGISTER_LINK = "role=link[name='Register']"
    LOGOUT_LINK = "role=link[name='Log out']"
    MY_ACCOUNT_LINK = "role=link[name='My account']"
    SEARCH_INPUT = "input[placeholder='Search store']"

    @allure.step("Open home page")
    def navigate_to_home(self):
        """Open the home page using base URL"""
        self.navigate()

    @allure.step("Open login form")
    def click_login(self):
        """Open the login form"""
        self.click(self.LOGIN_LINK)

    @allure.step("Open registration form")
    def click_register(self):
        """Open the registration form"""
        self.click(self.REGISTER_LINK)

    @allure.step("Log out user")
    def click_logout(self):
        """Log out current user"""
        self.click(self.LOGOUT_LINK)

    @allure.step("Assert home title contains brand")
    def assert_title(self):
        """Assert that title contains expected brand"""
        self.expect_title_contains("nopCommerce")

    def is_login_link_visible(self) -> bool:
        return self.is_visible(self.LOGIN_LINK)

    def is_register_link_visible(self) -> bool:
        return self.is_visible(self.REGISTER_LINK)

    def is_logout_link_visible(self) -> bool:
        return self.is_visible(self.LOGOUT_LINK)

    def is_my_account_visible(self) -> bool:
        return self.is_visible(self.MY_ACCOUNT_LINK)

    def is_user_logged_in(self) -> bool:
        return self.is_logout_link_visible() and self.is_my_account_visible()

    def is_user_logged_out(self) -> bool:
        return self.is_login_link_visible() and not self.is_logout_link_visible()
