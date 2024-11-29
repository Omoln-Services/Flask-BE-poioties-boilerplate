from api.v1.services.users import user_service
from api.utils.email_sender import send_reset_email


def test_reset_password_success(mocker, client, mock_user):
    """mock user successful request reset password
    """
    mocker.patch.object(user_service, "get_user_by_email", return_value=mock_user)
    mocker.patch.object(user_service, "generate_reset_link", return_value="mocker_reset_link")
    mocker.patch("api.utils.email_sender", return_value=True)
    
    # define payload
    payload = {
        "email": mock_user.email
    }
    
    # send request to /reset-password
    res = client.post("/api/v1/users/password-reset", json=payload)
    
    response_json = res.get_json()
    
    print(f"json: {response_json}")
    
    # assertions to validate response
    assert res.status_code == 200




def test_generate_reset_link_fake_user(mocker, client):
    """mock user successful request reset password
    """
    mocker.patch.object(user_service, "get_user_by_email", return_value=None)
    
    # define payload
    payload = {
        "email": "ma@gmail.com"
    }
    
    # send request to /reset-password
    res = client.post("/api/v1/users/password-reset", json=payload)
    
    response_json = res.get_json()
    
    print(f"json: {response_json}")
    
    # assertions to validate response
    assert res.status_code == 404




def test_invalid_email_format(mocker, client):
    """Test password reset with invalid email format"""
    
    mocker.patch.object(user_service, "post", return_value=None)
    
    # Define payload with invalid email
    payload = {
        "email": "invalid-email-format"
    }
    
    # Send request to /password-reset
    res = client.post("/api/v1/users/password-reset", json=payload)
    
    
    # Assertions to validate response
    assert res.status_code == 400


def test_missing_email(mocker, client):
    """Test password reset with missing email"""
    
    mocker.patch.object(user_service, "post", return_value=None)
    
    # Define payload with no email
    payload = {}
    
    # Send request to /password-reset
    res = client.post("/api/v1/users/password-reset", json=payload)
        
    # Assertions to validate response
    assert res.status_code == 400