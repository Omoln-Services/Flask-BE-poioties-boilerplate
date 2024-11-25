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

    print(res.get_json())

    # Assertions to validate response
    assert res.status_code == 200
    response_json = res.get_json()

    # Verify the presence of token in the response data
    assert "token" in response_json["data"]
