#!/usr/bin/env python3

# Import
from unittest import mock
import pytest
from app import create_app
from api.v1.models.users import User
from api.v1.services.users import user_service


@pytest.fixture(scope="session")
def client():
    """Create an instance of the Flask app."""
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        with app.test_client() as client:
            yield client
    if not app.config.get("SECRET_KEY"):
        raise ValueError("SECRET_KEY is not set in the .env")


@pytest.fixture(scope="function")
def mock_user():
    """Fixture to mock the User model."""
    # Create a mock user object
    mock_user = mock.Mock(spec=User)
    mock_user.id = "c9b6d7cd-08bc-450a-b972-dc7cf75e3401"
    mock_user.first_name = "John"
    mock_user.last_name = "Doe"
    mock_user.username = "john"
    mock_user.email = "johndoe@example.com"
    mock_user.is_active = True
    mock_user.is_deleted = False
    mock_user.is_superadmin = False
    mock_user.last_login = "2024-11-14T00:08:33.843367"

    return mock_user


@pytest.fixture(scope="function")
def mock_jwt_token(mocker):
    """Fixture to mock JWT token generation."""
    mock_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMjUwMDQ2MywianRpIjoiMDk3YTMxMmYtMTgyMi00YWEwLWFhN2UtZTMzZTJhMTBhODUxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImM5YjZkN2NkLTA4YmMtNDUwYS1iOTcyLWRjN2NmNzVlMzQwMSIsIm5iZiI6MTczMjUwMDQ2MywiY3NyZiI6IjY3Y2JiZjRmLWM0OGItNGEzNi1hMzExLTNmZTY2ODYxNmE2ZiIsImV4cCI6MTczMjUwNDA2MywiZW1haWwiOiJqb2huQGV4YW1wbGUuY29tIn0.cVWRpqnkvXElSUhXq897SX4uYY4NLMDrdBiIPuixuyU"

    # Mock the JWT token generation method to return the fake token
    mocker.patch.object(user_service, "generate_jwt_token", return_value=mock_token)

    return mock_token



@pytest.fixture(scope="function")
def mock_reset_link(mocker):
    """Fixture to mock password reset token generation."""
    mock_reset_link = "http://127.0.0.1:7000/api/v1/users/password-reset/verify?token=eyJpZCI6ImU5NTViMjQ1LTkxYmEtNDAyYS05Nzc4LWMzNDI3NTJhMTJiNSJ9.Z0PCGw.4bJKyWcimpRxMeL0e6x7VE4eXY8"

    # Mock the JWT token generation method to return the fake token
    mocker.patch.object(user_service, "generate_reset_link", return_value=mock_reset_link)

    return mock_reset_link
