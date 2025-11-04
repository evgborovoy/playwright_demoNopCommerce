import allure


@allure.suite("Smoke")
class TestRegistrationSmoke:
    def test_registration_page_accessible_from_home(self, register_page):
        register_page.navigate_to_register()
        assert register_page.is_visible(register_page.REGISTER_BUTTON)
