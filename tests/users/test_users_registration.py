from unittest.mock import MagicMock
from flask import Flask
import pytest
from app import create_app
from api.v1.services.users import user_service


@pytest.fixture
def client():
    """ create an instance of the flask app """
    app = create_app()
    app.config['TESTING'] = True
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