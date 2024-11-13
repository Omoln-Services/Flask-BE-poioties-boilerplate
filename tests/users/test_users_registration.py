from unittest.mock import MagicMock
from flask import Flask
import pytest
from app import create_app
from api.v1.services.users import user_service


@pytest.fixture(scope='session')
def client():
    """ create an instance of the flask app """
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        with app.test_client() as client:
            yield client

def test_register_success(mocker, client):
    """ Mock the user service post method to return successful response """
    mock_response = {
        "message": "User registrated successfully",
        "status": "success",
        "data": {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com"
        }
    }
    
    mocker.patch.object(user_service, 'post', return_value=(mock_response, 201))
    
    # Define the payload to send in the request
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "password": "password123",
        "email": "johndoe@example.com"
    }
    
    # send request to /register
    res = client.post('/api/v1/users/register', json=payload)
    
    # Assertions to validate response
    assert res.status_code == 201
    


def test_register_validation_error(mocker, client):
    """ Mock the user_service post method to simulate a validation error response"""
    mock_response = {
        "status_code": 400,
        "message": "Missing required fields",
        "success": False
    }
    
    mocker.patch.object(user_service, 'post', return_value=(mock_response, 400))
    
    # incomplete payload to simulate validation failure
    payload = {
        "last_name": "Doe",
        "username": "johndoe",
        "email": "johndoe@example.com"
    }

    # Send POST request to /register route
    res = client.post('api/v1/users/register', json=payload)
    
    # Assertions to validate response
    assert res.status_code == 400

    
    
def test_existing_email_or_username(mocker, client):
    """Mock the user service post method to simulate existing email or username."""
    mock_response = {
        "status_code": 409,
        "message": "Email or username already exists",
        "success": False
    }
    
    # Mock the `post` method of `user_service` to return the conflict response
    mocker.patch.object(user_service, 'post', return_value=(mock_response, 409))
    
    # Define a payload with an email or username that already exists
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "username": "johndoe",
        "password": "password123",
        "email": "johndoe@example.com"
    }
    
    # Send POST request to /register route
    res = client.post('/api/v1/users/register', json=payload)
    
    # Assertions to validate response
    assert res.status_code == 409
    
    
    
def test_register_internal_server_error(mocker, client):
    """Mock the user service post method to simulate an internal server error."""
    mock_response = {
        "status_code": 500,
        "message": "Internal server error",
        "success": False
    }
    
    mocker.patch.object(user_service, 'post', return_value=(mock_response, 500))
    
    # Define a valid payload for registration
    payload = {
        "first_name": "Alice",
        "last_name": "Smith",
        "username": "alicesmith",
        "password": "password123",
        "email": "alice@example.com"
    }
    
    # Send POST request to /register route
    res = client.post('/api/v1/users/register', json=payload)
    
    # Assertions to validate response
    assert res.status_code == 500