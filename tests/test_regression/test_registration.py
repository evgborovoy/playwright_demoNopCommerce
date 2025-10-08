import pytest
from config.test_data import TestData


class TestRegistration:
    """
    Regression tests for user registration functionality
    """

    def test_registration_page_loading(self, register_page):
        assert register_page.is_visible(register_page.FIRST_NAME_INPUT)
        assert register_page.is_visible(register_page.LAST_NAME_INPUT)
        assert register_page.is_visible(register_page.EMAIL_INPUT)
        assert register_page.is_visible(register_page.PASSWORD_INPUT)
        assert register_page.is_visible(register_page.REGISTER_BUTTON)
        register_page.logger.info("Registration page loads correctly")

    def test_registration_with_valid_data(self, register_page, home_page):
        user_data = TestData.generate_user_data()
        register_page.register(user_data)
        assert register_page.is_registration_successful(), "Registration should be successful"
        register_page.click_continue()
        assert "nopCommerce" in home_page.get_page_title()
        register_page.logger.info(f"Registration successful for: {user_data['email']}")

    def test_registration_with_female_gender(self, register_page, home_page):
        user_data = TestData.generate_user_data(gender="female")
        register_page.register(user_data)
        assert register_page.is_registration_successful()
        register_page.click_continue()
        assert home_page.is_user_logged_in()
        register_page.logger.info("Female registration works correctly")

    @pytest.mark.parametrize("scenario_name,user_data,expected_errors",
                             TestData.generate_invalid_user_data_scenarios())
    def test_registration_validation_errors(self, register_page, scenario_name, user_data, expected_errors):
        register_page.register(user_data)
        validation_errors = register_page.get_validation_errors()
        assert len(validation_errors) >= expected_errors, \
            f"Scenario '{scenario_name}' should show at least {expected_errors} validation error(s)"

        register_page.logger.info(f"Validation scenario '{scenario_name}' works correctly")

    def test_registration_with_weak_passwords(self, register_page):
        weak_passwords = TestData.get_weak_passwords()

        for weak_password in weak_passwords:
            user_data = TestData.generate_user_data()
            user_data.update({
                "password": weak_password,
                "confirm_password": weak_password
            })
            register_page.register(user_data)
            validation_errors = register_page.get_validation_errors()
            assert validation_errors, f"Weak password '{weak_password}' should show validation error"
            register_page.logger.info(f"Weak password '{weak_password}' correctly shows error")

    def test_duplicate_email_registration(self, register_page):
        user_data = TestData.generate_user_data()
        # first registration
        register_page.register(user_data)
        assert register_page.is_registration_successful()
        register_page.click_continue()

        # second registration with same email
        register_page.navigate_to_register()
        register_page.register(user_data)

        error_messages = register_page.get_error_messages()
        assert any("already exists" in error.lower() for error in error_messages)
        register_page.logger.info("Duplicate email registration correctly fails")


class TestRegistrationBoundary:
    """
    Tests for boundary cases in registration
    """

    def test_registration_with_long_names(self, register_page):
        user_data = TestData.generate_user_data()
        user_data.update({
            "first_name": "A" * 100,
            "last_name": "B" * 100
        })

        register_page.register(user_data)

        success = register_page.is_registration_successful()
        errors = register_page.get_validation_errors()

        assert success or errors, "Should either succeed or show validation errors"
        register_page.logger.info("Long names handled correctly")
