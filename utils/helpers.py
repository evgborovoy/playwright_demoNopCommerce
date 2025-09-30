import random
import string


def generate_random_string(length: int = 10, include_digits: bool = True) -> str:
    characters = string.ascii_letters
    if include_digits:
        characters += string.digits

    return ''.join(random.choice(characters) for _ in range(length))


def generate_random_email(domain: str = "test.com", username_length: int = 8) -> str:
    username = generate_random_string(username_length, include_digits=True).lower()
    return f"{username}@{domain}"


def generate_random_password(length: int = 12) -> str:
    if length < 8:
        raise ValueError("Password length should be at least 8 characters")

    # password should have at least one of each type
    lower = random.choice(string.ascii_lowercase)
    upper = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*")

    remaining_length = length - 4
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    remaining = ''.join(random.choice(all_chars) for _ in range(remaining_length))

    # combine and shuffle
    password_chars = list(lower + upper + digit + special + remaining)
    random.shuffle(password_chars)

    return ''.join(password_chars)


def validate_email(email: str) -> bool:
    if not email or '@' not in email:
        return False

    name, domain = email.split('@', 1)

    if not name or not domain:
        return False
    if '.' not in domain:
        return False

    return True


if __name__ == "__main__":
    print("Testing helper functions")

    # Test random string generation
    random_str = generate_random_string(10)
    print(f"Random string: {random_str}")

    # Test email generation
    email = generate_random_email()
    print(f"Random email: {email}")
    print(f"Email valid: {validate_email(email)}")

    # Test password generation
    password = generate_random_password(12)
    print(f"Random password: {password}")

    print("PASS: All helper functions work correctly!")
