from .base_page import BasePage


class HomePage(BasePage):
    LOGIN_LINK = "text=Log in"
    REGISTER_LINK = "text=Register"
    SEARCH_BOX = "#small-searchterms"
    LOGOUT_LINK = "text=Log out"
    MY_ACCOUNT_LINK = "text=My account"

    def navigate_to_home(self):
        self.navigate()

    def click_login(self):
        self.click(self.LOGIN_LINK)

    def click_register(self):
        self.click(self.REGISTER_LINK)

    def get_page_title(self) -> str:
        return self.page.title()

    def is_login_link_visible(self) -> bool:
        return self.is_visible(self.LOGIN_LINK)

    def is_register_link_visible(self) -> bool:
        return self.is_visible(self.REGISTER_LINK)

    def is_logout_link_visible(self) -> bool:
        return self.is_visible(self.LOGOUT_LINK)

    def wait_for_login_state(self, should_be_logged_in: bool = True, timeout: int = 5000):
        self.logger.info(f"Waiting for user to be {'logged in' if should_be_logged_in else 'logged out'}")

        if should_be_logged_in:
            self.page.wait_for_selector(self.LOGOUT_LINK, timeout=timeout)
        else:
            self.page.wait_for_selector(self.LOGIN_LINK, timeout=timeout)

        self.logger.info(f"User is {'logged in' if should_be_logged_in else 'logged out'}")

    def is_my_account_visible(self) -> bool:
        return self.is_visible(self.MY_ACCOUNT_LINK)

    def is_user_logged_in(self) -> bool:
        return self.is_logout_link_visible() and self.is_my_account_visible()

    def is_user_logged_out(self) -> bool:
        return self.is_login_link_visible() and not self.is_logout_link_visible()
