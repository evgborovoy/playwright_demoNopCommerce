import pytest


@pytest.mark.smoke
class TestRegistrationSmoke:
    """
    Smoke tests for registration functionality
    """

    def test_registration_page_accessible_from_home(self, home_page, register_page):
        home_page.navigate_to_home()
        home_page.click_register()
        assert register_page.is_visible(register_page.REGISTER_BUTTON)
        register_page.logger.info("Registration page accessible from home")
