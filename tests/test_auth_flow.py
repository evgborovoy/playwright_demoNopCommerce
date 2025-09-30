from config.test_data import TestData


def test_complete_auth_flow(home_page, register_page, login_page):
    """
    Test complete authentication flow using centralized test data
    """

    user_data = TestData.generate_user_data()

    # Registration
    home_page.navigate_to_home()
    home_page.click_register()
    register_page.register(user_data)
    assert register_page.is_registration_successful()
    register_page.click_continue()

    # Verify logged in after registration
    assert home_page.is_user_logged_in()

    # Logout
    home_page.click_logout()
    assert home_page.is_user_logged_out()

    # Login with registered credentials
    home_page.click_login()
    login_page.login(user_data["email"], user_data["password"])

    # Verify logged in again
    assert home_page.is_user_logged_in()

    print(f"Complete auth flow successful for: {user_data['email']}")
