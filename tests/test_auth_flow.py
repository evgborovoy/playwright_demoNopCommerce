import allure
from config.test_data import TestData


@allure.suite("Auth")
@allure.title("Register -> Logout -> Login (happy path)")
def test_complete_auth_flow(home_page, register_page, login_page):
    """
    Full happy-path:
    - Register
    - Logout
    - Login back
    - Validate session state via HomePage
    """
    user_data = TestData.generate_user_data()

    # register
    home_page.navigate_to_home()
    home_page.click_register()
    register_page.register(user_data)
    assert register_page.is_registration_successful()
    register_page.click_continue()
    assert home_page.is_user_logged_in()

    # logout
    home_page.click_logout()
    assert home_page.is_user_logged_out()

    # login
    home_page.click_login()
    login_page.login(user_data["email"], user_data["password"])
    assert home_page.is_user_logged_in()
