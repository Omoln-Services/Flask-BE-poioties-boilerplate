from unittest.mock import MagicMock
from flask import Flask
import pytest
from flask_jwt_extended import create_access_token

from app import create_app
from api.v1.services.users import user_service


@pytest.fixture(scope="session")
def client():
    """create an instance of the flask app"""
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        with app.test_client() as client:
            yield client
    if not app.config.get("SECRET_KEY"):
        raise ValueError("SECRET_KEY is not set in the environment variables")


def test_register_success(mocker, client):
    """Mock the user service post method to return successful response"""
    mock_response = {
        "message": "User registrated successfully",
        "status": "success",
        "data": {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
        },
    }

    mocker.patch.object(user_service, "post", return_value=(mock_response, 201))

    # Define the payload to send in the request
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "password": "password123",
        "email": "johndoe@example.com",
    }

    # send request to /register
    res = client.post("/api/v1/users/register", json=payload)

    # Assertions to validate response
    assert res.status_code == 201


def test_register_validation_error(mocker, client):
    """Mock the user_service post method to simulate a validation error response"""
    mock_response = {
        "status_code": 400,
        "message": "Missing required fields",
        "success": False,
    }

    mocker.patch.object(user_service, "post", return_value=(mock_response, 400))

    # incomplete payload to simulate validation failure
    payload = {
        "last_name": "Doe",
        "username": "johndoe",
        "email": "johndoe@example.com",
    }

    # Send POST request to /register route
    res = client.post("api/v1/users/register", json=payload)

    # Assertions to validate response
    assert res.status_code == 400


def test_existing_email_or_username(mocker, client):
    """Mock the user service post method to simulate existing email or username."""
    mock_response = {
        "status_code": 409,
        "message": "Email or username already exists",
        "success": False,
    }

    # Mock the `post` method of `user_service` to return the conflict response
    mocker.patch.object(user_service, "post", return_value=(mock_response, 409))

    # Define a payload with an email or username that already exists
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "username": "johndoe",
        "password": "password123",
        "email": "johndoe@example.com",
    }

    # Send POST request to /register route
    res = client.post("/api/v1/users/register", json=payload)

    # Assertions to validate response
    assert res.status_code == 409


def test_register_internal_server_error(mocker, client):
    """Mock the user service post method to simulate an internal server error."""
    mock_response = {
        "status_code": 500,
        "message": "Internal server error",
        "success": False,
    }

    mocker.patch.object(user_service, "post", return_value=(mock_response, 500))

    # Define a valid payload for registration
    payload = {
        "first_name": "Alice",
        "last_name": "Smith",
        "username": "alicesmith",
        "password": "password123",
        "email": "alice@example.com",
    }

    # Send POST request to /register route
    res = client.post("/api/v1/users/register", json=payload)

    # Assertions to validate response
    assert res.status_code == 500


def test_get_user_profile_success(mocker, client):
    """Mock user to get method to stimulate a user profile and get a success response"""
    test_user_id = "7c1bd1f8-19d3-4370-9061-30985bb46e5f"
    token = create_access_token(identity=test_user_id)
    mock_response = {
        "status_code": 200,
        "message": "User retrieved Successfully",
        "data": {
            "id": "7c1bd1f8-19d3-4370-9061-30985bb46e5f",
            "created_at": "2024-11-15 14:42:12.033666",
            "email": "yonwatodejulius@gmail.com",
            "avatar_url": None,
            "is_active": True,
            "username": "skibo555",
        }
    }
    headers = {"Authorization": f"Bearer {token}"}

    mocker.patch.object(user_service, "get", return_value=(mock_response, 200), headers=headers)
    
    # Send get request to /register route
    res = client.get("/api/v1/users/me", headers=headers)
    
    assert res.status_code == 200


def test_get_user_profile_invalid_token(mocker, client):
    """Mock user with a non-existence user_id to get method to stimulate a user profile and get 404 error"""
    test_user_id = "7c1bd1f8-19d3-4370-9061-30985bb46e5t"
    token = create_access_token(identity=test_user_id)
    mock_response = {
        "status_code": 404,
        "message": "User profile not found",
    }
    headers = {"Authorization": f"Bearer {token}"}

    mocker.patch.object(user_service, "get", return_value=(mock_response, 404), headers=headers)

    # Send get request to /me route
    res = client.get("/api/v1/users/me", headers=headers)

    # Print the response data
    print(f"Status Code: {res.status_code}")
    print(f"Response Data: {res}")

    assert res.status_code == 404

