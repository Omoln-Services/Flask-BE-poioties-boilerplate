from api.v1.services.users import user_service


def test_user_success_login(mocker, client, mock_user, mock_jwt_token):
    """Mock the user service post method to return successful response"""
    # Mock the response from the user service authenticate method
    mock_response = {
        "avatar_url": "",
        "first_name": mock_user.first_name,
        "id": mock_user.id,
        "is_active": mock_user.is_active,
        "is_deleted": mock_user.is_deleted,
        "is_superadmin": mock_user.is_superadmin,
        "last_login": mock_user.last_login,
        "last_name": mock_user.last_name,
        "token": mock_jwt_token,
        "username": mock_user.username,
    }

    mocker.patch.object(user_service, "authenticate", return_value=mock_response)

    # Define the payload to send in the request
    payload = {
        "password": "password123",
        "email": "johndoe@example.com",
    }

    # send request to /register
    res = client.post("/api/v1/users/login", json=payload)

    # Assertions to validate response
    assert res.status_code == 200
    response_json = res.get_json()

    # Verify the token in the response data
    assert "token" in response_json["data"]


def test_invalid_credential_login(mocker, client):
    """Mock the user_service post method to simulate a validation error response"""

    mock_response = {
        "status_code": 401,
        "message": "Invalid email or password",
        "success": False,
    }

    mocker.patch.object(user_service, "authenticate", return_value=mock_response)

    # incomplete payload to simulate validation failure
    payload = {"email": "jone@gmail.com", "password": "word123"}

    # Send POST request to /register route
    res = client.post("api/v1/users/login", json=payload)

    response_json = res.get_json()

    print(f"json: {response_json}")

    # Assertions to validate response
    assert res.status_code == 401


def test_Missing_credential_login(mocker, client):
    """Mock the user_service post method to simulate a validation error response"""

    mock_response = {
        "status_code": 400,
        "message": "Email and password are required",
        "success": False,
    }

    mocker.patch.object(user_service, "authenticate", return_value=mock_response)

    # incomplete payload to simulate validation failure
    payload = {"password": "word123"}

    # Send POST request to /register route
    res = client.post("api/v1/users/login", json=payload)

    response_json = res.get_json()

    print(f"json: {response_json}")

    # Assertions to validate response
    assert res.status_code == 400


def test_services_credential_login(mocker, client):
    """Mock the user_service post method to simulate a validation error response"""

    mock_response = {
        "status_code": 500,
        "message": "Social login failed. Try again.",
        "success": False,
    }

    mocker.patch.object(user_service, "authenticate", return_value=mock_response)

    # incomplete payload to simulate validation failure
    payload = {"email": "jone@gmail.com", "password": "word123"}

    # Send POST request to /register route
    res = client.post("api/v1/users/login", json=payload)

    response_json = res.get_json()

    print(f"json: {response_json}")

    # Assertions to validate response
    assert res.status_code == 500
