class TestData:
    """Test data for authentication tests"""

    # Invalid test data
    INVALID_CREDENTIALS = [
        {"email": "invalid@example.com", "password": "wrongpassword"},
        {"email": "test@example.com", "password": ""},  # empty password
        {"email": "", "password": "password123"},  # empty email
    ]