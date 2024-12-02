from api.v1.services.users import user_service, create_access_token


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
        },
    }
    headers = {"Authorization": f"Bearer {token}"}

    mocker.patch.object(
        user_service, "get", return_value=(mock_response, 200), headers=headers
    )

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

    mocker.patch.object(
        user_service, "get", return_value=(mock_response, 404), headers=headers
    )

    # Send get request to /me route
    res = client.get("/api/v1/users/me", headers=headers)

    # Print the response data
    print(f"Status Code: {res.status_code}")
    print(f"Response Data: {res}")

    assert res.status_code == 404
