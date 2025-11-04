import allure
from pages.base_page import BasePage


class RegisterPage(BasePage):
    GENDER_MALE = "#gender-male"
    GENDER_FEMALE = "#gender-female"
    FIRST_NAME_INPUT = "//input[@id='FirstName']"
    LAST_NAME_INPUT = "//input[@id='LastName']"
    EMAIL_INPUT = "#Email"
    PASSWORD_INPUT = "#Password"
    CONFIRM_PASSWORD_INPUT = "#ConfirmPassword"
    REGISTER_BUTTON = "#register-button"
    SUCCESS_MESSAGE = ".result"
    CONTINUE_BUTTON = "role=link[name='Continue']"

    @allure.step("Open register page")
    def navigate_to_register(self):
        """Open /register and wait for the form"""
        self.navigate("/register")
        self.expect_visible(self.FIRST_NAME_INPUT)

    @allure.step("Select gender: {gender}")
    def select_gender(self, gender: str = "male"):
        """Pick gender toggle based on input (male/female)"""
        gender = gender.lower()
        self.click(self.GENDER_MALE if gender == "male" else self.GENDER_FEMALE)

    @allure.step("Fill personal data")
    def fill_personal_data(self, first_name: str, last_name: str, email: str):
        """Fill personal data fields"""
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.EMAIL_INPUT, email)

    @allure.step("Fill passwords")
    def fill_passwords(self, password: str, confirm_password: str | None = None):
        """Fill password and confirmation (defaults to same value)"""
        confirm = confirm_password or password
        self.fill(self.PASSWORD_INPUT, password)
        self.fill(self.CONFIRM_PASSWORD_INPUT, confirm)

    @allure.step("Submit registration form")
    def submit(self):
        """Submit registration form"""
        self.click(self.REGISTER_BUTTON)

    @allure.step("Register user (happy path)")
    def register(self, user_data: dict):
        """Full happy-path registration using provided data dict"""
        self.navigate_to_register()
        self.select_gender(user_data.get("gender", "male"))
        self.fill_personal_data(user_data["first_name"], user_data["last_name"], user_data["email"])
        self.fill_passwords(user_data["password"])
        self.submit()

    def is_registration_successful(self) -> bool:
        """Detect success banner presence"""
        return self.is_visible(self.SUCCESS_MESSAGE)

    @allure.step("Continue after successful registration")
    def click_continue(self):
        """Continue to home after successful registration"""
        self.click(self.CONTINUE_BUTTON)
