from .base_page import BasePage


class HomePage(BasePage):
    LOGIN_LINK = "text=Log in"
    REGISTER_LINK = "text=Register"
    SEARCH_BOX = "#small-searchterms"

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
