#!/usr/bin/env python3

# Import
from flask import request
from flask_restx import Resource, fields
from werkzeug.security import generate_password_hash
from api.utils.success_response import success_response
from api.v1.models.users import User
from api.utils.email_validator import validate_email
from api.v1.services.users import user_service
from api.utils.email_sender import send_reset_email
from api.db.database import db
from . import user_ns


password_model = user_ns.model(
    "password-reset",
    {
        "email": fields.String(required=True, description="user email"),
    },
)


@user_ns.route("/password-reset")
class PasswordResetRequest(Resource):
    """user login docs with flask restx"""

    @user_ns.expect(password_model, validate=True)
    @user_ns.doc(description="Api that handles user password reset")
    @user_ns.response(200, "Password reset link sent to your email")
    @user_ns.response(404, "User not found")
    @user_ns.response(400, "Email is required and must be a valid format")
    @user_ns.response(500, "Internal server error")
    def post(self):
        """Handle password reset requests"""
        email = request.json.get("email")

        # Validate email presence and format
        if not email:
            return success_response(
                status_code=400, message="Email is required and must be a valid format"
            )

        if not validate_email(email):
            return success_response(status_code=400, message="Invalid email format")

        # Fetch user by email
        user = user_service.get_user_by_email(email)
        if not user:
            return success_response(status_code=404, message="User not found")

        # Generate reset token and link
        reset_link = user_service.generate_reset_link(user)

        # Send the email
        if send_reset_email(user, reset_link):
            return success_response(
                status_code=200, message="Password reset link sent to your email"
            )


verify_token_model = user_ns.model(
    "verify-token",
    {"token": fields.String(required=True, description="Password Reset Token")},
)


@user_ns.route("/password-reset/verify")
class PasswordResetVerify(Resource):
    """class to verify password reset token"""

    @user_ns.expect(verify_token_model, Validation=True)
    @user_ns.doc(description="API that handles user password reset token verification")
    @user_ns.response(404, "User not found")
    @user_ns.response(400, "Token is required")
    @user_ns.response(500, "Invalid or expired token")
    def get(self):
        """Verify the password reset token"""
        token = request.args.get("token")

        if not token:
            return success_response(status_code=400, message="Token is required.")

        # verify the token
        user_id = user_service.verify_reset_token(token)

        # check if user exist
        user = db.session.get(User, user_id)
        if not user:
            return success_response(status_code=404, message="User not found.")

        return success_response(
            status_code=200, message="valid Token", data={"user_id": user_id}
        )


confirm_password_model = user_ns.model(
    "confirm-token",
    {
        "token": fields.String(required=True, description="Token"),
        "new_password": fields.String(required=True, description="new password"),
        "confirm_password": fields.String(
            required=True, description="confirm password"
        ),
    },
)


@user_ns.route("/password-reset/confirm")
class PasswordResetConfirm(Resource):
    """Verify the password reset token"""

    @user_ns.expect(confirm_password_model, Validation=True)
    @user_ns.doc(
        description="API that handles user password reset token \
        verificationand password update"
    )
    @user_ns.response(404, "User not found")
    @user_ns.response(400, "Token is required or Password mismatch")
    @user_ns.response(422, "Password is too short")
    @user_ns.response(500, "Invalid or expired token")
    def post(self):
        """Change the password using the reset token"""
        token = request.json.get("token")
        new_password = request.json.get("new_password")
        confirm_password = request.json.get("confirm_password")

        # check token
        if not token:
            return success_response(status_code=400, message="Token is required.")

        # Validate the presence and match of passwords
        if not new_password or len(new_password) < 3:
            return success_response(
                status_code=422, message="Password must be at least 3 characters long."
            )

        if new_password != confirm_password:
            return success_response(status_code=400, message="Passwords do not match.")

        user = user_service.get_user_by_reset_token(token)

        # Check if the user exists
        if not user:
            return success_response(status_code=404, message="User not found.")

        # Update the user's password
        user.password = generate_password_hash(new_password)
        db.session.commit()

        return success_response(
            status_code=200, message="Password updated successfully."
        )
