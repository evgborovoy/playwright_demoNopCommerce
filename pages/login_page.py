import allure
from pages.base_page import BasePage


class LoginPage(BasePage):
    EMAIL_INPUT = "#Email"
    PASSWORD_INPUT = "#Password"
    LOGIN_BUTTON = "role=button[name='Log in']"
    REMEMBER_ME_CHECKBOX = "#RememberMe"
    ERROR_MESSAGE = ".message-error"
    FORGOT_PASSWORD_LINK = "role=link[name='Forgot password?']"

    @allure.step("Open login page")
    def navigate_to_login(self):
        """Open /login and wait for essential controls"""
        self.navigate("login")
        self.wait_for_login_form()

    @allure.step("Wait for login form")
    def wait_for_login_form(self):
        """Ensure form inputs are visible before interacting"""
        self.expect_visible(self.EMAIL_INPUT)
        self.expect_visible(self.PASSWORD_INPUT)

    @allure.step("Submit login credentials")
    def login(self, email: str, password: str, remember_me: bool = False):
        """Fill credentials and submit the form"""
        if not self.is_visible(self.EMAIL_INPUT):
            self.navigate_to_login()
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        if remember_me:
            self.click(self.REMEMBER_ME_CHECKBOX)
        self.click(self.LOGIN_BUTTON)

    @allure.step("Click 'Forgot password?' link")
    def click_forgot_password(self):
        """Open password recovery flow"""
        if not self.is_visible(self.FORGOT_PASSWORD_LINK):
            self.navigate_to_login()
        self.click(self.FORGOT_PASSWORD_LINK)

    @allure.step("Read login error message")
    def get_error_message(self) -> str:
        if self.is_visible(self.ERROR_MESSAGE):
            text = self.get_text(self.ERROR_MESSAGE).strip()
            self.logger.info(f"[LOGIN ERROR] {text}")
            return text
        return ""

    def is_login_page_loaded(self) -> bool:
        return self.is_visible(self.EMAIL_INPUT) and self.is_visible(self.PASSWORD_INPUT)
