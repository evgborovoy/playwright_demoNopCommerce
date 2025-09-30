from faker import Faker

fake = Faker()


class TestData:

    @staticmethod
    def generate_user_data(gender: str = "male", include_company: bool = False):
        first_name = fake.first_name_male() if gender == "male" else fake.first_name_female()
        last_name = fake.last_name()
        email = fake.email()

        user_data = {
            "gender": gender,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": "Test123!",
            "confirm_password": "Test123!"
        }

        if include_company:
            user_data["company"] = fake.company()

        return user_data

    @staticmethod
    def generate_invalid_user_data_scenarios():
        base_data = TestData.generate_user_data()

        scenarios = [
            (
                "empty_first_name",
                {**base_data, "first_name": ""},
                1  # expected 1 error in scenario
            ),
            (
                "empty_last_name",
                {**base_data, "last_name": ""},
                1
            ),
            (
                "empty_email",
                {**base_data, "email": ""},
                1
            ),
            (
                "password_mismatch",
                {**base_data, "confirm_password": "Different123!"},
                1
            ),
            (
                "weak_password",
                {**base_data, "password": "123", "confirm_password": "123"},
                1
            ),
        ]

        return scenarios

    @staticmethod
    def get_existing_user_data():
        """
        Get test data for already registered user.
        In real project, this would come from test database or API.
        """
        return {
            "email": "test@example.com",  # This should be pre-registered in test environment
            "password": "Password123!"
        }

    @staticmethod
    def get_weak_passwords():
        return [
            "123",  # Too short
            "password",  # Common password
            "abc",  # No uppercase/digits/special
            "TEST123",  # No lowercase
            "TestTest"  # No digits/special
        ]

    @staticmethod
    def get_invalid_emails():
        return [
            "invalid-email",
            "missing@domain",
            "@missinglocal.com",
            "spaces in@email.com"
        ]
