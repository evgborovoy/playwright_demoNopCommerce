from pages.base_page import BasePage


class LoginPage(BasePage):
    EMAIL_INPUT = "#Email"
    PASSWORD_INPUT = "#Password"
    LOGIN_BUTTON = "button:has-text('Log in')"
    REMEMBER_ME_CHECKBOX = "#RememberMe"
    ERROR_MESSAGE = ".message-error"
    FORGOT_PASSWORD_LINK = "text=Forgot password?"

    def navigate_to_login(self):
        self.navigate("login")
        self.wait_for_login_form()

    def wait_for_login_form(self):
        self.logger.info("Waiting for login form")
        self.page.wait_for_selector(self.EMAIL_INPUT, state="visible")
        self.logger.info("Login form is visible")

    def login(self, email: str, password: str, remember_me: bool = False):
        self.logger.info(f"Logging in with email: {email}")
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)

        if remember_me:
            self.click(self.REMEMBER_ME_CHECKBOX)

        self.click(self.LOGIN_BUTTON)
        self.logger.info("Login attempt completed")

    def get_error_message(self) -> str:
        if self.is_visible(self.ERROR_MESSAGE):
            error_text = self.get_text(self.ERROR_MESSAGE)
            self.logger.info(f"Login error: {error_text}")
            return error_text
        return ""

    def click_forgot_password(self):
        self.logger.info("Clicking forgot password link")
        self.click(self.FORGOT_PASSWORD_LINK)

    def is_login_page_loaded(self) -> bool:
        return self.is_visible(self.EMAIL_INPUT) and self.is_visible(self.PASSWORD_INPUT)

    def is_login_successful(self, home_page) -> bool:
        home_page.wait_for_login_state(should_be_logged_in=True)
        return home_page.is_user_logged_in()
