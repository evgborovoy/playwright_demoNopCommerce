from pages.base_page import BasePage


class RegisterPage(BasePage):
    GENDER_MALE = "#gender-male"
    GENDER_FEMALE = "#gender-female"
    FIRST_NAME_INPUT = "#FirstName"
    LAST_NAME_INPUT = "#LastName"
    EMAIL_INPUT = "#Email"
    PASSWORD_INPUT = "#Password"
    CONFIRM_PASSWORD_INPUT = "#ConfirmPassword"
    REGISTER_BUTTON = "#register-button"
    SUCCESS_MESSAGE = ".result"
    CONTINUE_BUTTON = "text=Continue"

    ERROR_MESSAGES = ".message-error"
    VALIDATION_ERRORS = ".field-validation-error"

    def wait_for_register_form(self):
        self.logger.info("Waiting for registration form")
        self.page.wait_for_selector(self.FIRST_NAME_INPUT, state="visible")
        self.logger.info("Registration form is visible")

    def navigate_to_register(self):
        self.navigate("/register")
        self.wait_for_register_form()

    def select_gender(self, gender: str = "male"):
        gender = gender.lower()
        if gender == "male":
            self.click(self.GENDER_MALE)
        elif gender == "female":
            self.click(self.GENDER_FEMALE)

        self.logger.info(f"Selected gender: {gender}")

    def fill_personal_data(self, first_name: str, last_name: str, email: str):
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.EMAIL_INPUT, email)
        self.logger.info(f"Filled personal details for: {first_name} {last_name}")

    def fill_password(self, password: str, confirm_password: str = None):
        if confirm_password is None:
            confirm_password = password

        self.fill(self.PASSWORD_INPUT, password)
        self.fill(self.CONFIRM_PASSWORD_INPUT, confirm_password)
        self.logger.info("Filled password fields")

    def register(self, user_data: dict):
        self.logger.info(f"Starting registration for: {user_data.get('email', 'unknown')}")

        if user_data.get('gender'):
            self.select_gender(user_data['gender'])

        self.fill_personal_data(
            user_data['first_name'],
            user_data['last_name'],
            user_data['email']
        )

        self.fill_password(
            user_data['password'],
            user_data.get('confirm_password', user_data['password'])
        )

        self.click(self.REGISTER_BUTTON)
        self.logger.info("Registration form submitted")

    def get_success_message(self) -> str:
        if self.is_visible(self.SUCCESS_MESSAGE):
            message = self.get_text(self.SUCCESS_MESSAGE)
            self.logger.info(f"Registration success: {message}")
            return message
        return ""

    def get_error_messages(self) -> list:
        errors = []
        for error_element in self.page.locator(self.ERROR_MESSAGES).all():
            error_text = error_element.text_content()
            if error_text:
                errors.append(error_text)
                self.logger.error(f"Registration error: {error_text}")
        return errors

    def get_validation_errors(self) -> list:
        errors = []
        for error_element in self.page.locator(self.VALIDATION_ERRORS).all():
            error_text = error_element.text_content()
            if error_text:
                errors.append(error_text)
                self.logger.info(f"Validation error: {error_text}")
        return errors

    def click_continue(self):
        if self.is_visible(self.CONTINUE_BUTTON):
            self.click(self.CONTINUE_BUTTON)
            self.logger.info("Continued after registration")

    def is_registration_successful(self) -> bool:
        success_message = self.get_success_message()
        return bool(success_message and "Your registration completed" in success_message)
