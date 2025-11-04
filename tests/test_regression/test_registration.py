import allure
from config.test_data import TestData


@allure.suite("Registration")
class TestRegistration:
    @allure.title("Registration page shows essential controls")
    def test_registration_page_loading(self, register_page):
        register_page.navigate_to_register()
        """Basic presence of registration controls"""
        assert register_page.is_visible(register_page.FIRST_NAME_INPUT)
        assert register_page.is_visible(register_page.LAST_NAME_INPUT)
        assert register_page.is_visible(register_page.EMAIL_INPUT)
        assert register_page.is_visible(register_page.PASSWORD_INPUT)
        assert register_page.is_visible(register_page.REGISTER_BUTTON)

    @allure.title("Registration success with valid data")
    def test_registration_with_valid_data(self, register_page, home_page):
        """Valid registration leads to success banner and home"""
        user_data = TestData.generate_user_data()
        register_page.register(user_data)
        assert register_page.is_registration_successful()
        register_page.click_continue()
        home_page.assert_title()

    @allure.title("Registration also works with female gender")
    def test_registration_with_female_gender(self, register_page, home_page):
        """Alternate gender selection remains a happy path"""
        user_data = TestData.generate_user_data(gender="female")
        register_page.register(user_data)
        assert register_page.is_registration_successful()
        register_page.click_continue()
        home_page.assert_title()
