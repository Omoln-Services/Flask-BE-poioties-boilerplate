#!/usr/bin/env python3

# Import
from datetime import datetime, timedelta
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from api.utils.success_response import success_response
from api.utils.db_validator import check_model_existence
from api.core.base.services import Service
from api.v1.models.users import User
from api.db.database import db


class UserService(Service):
    """User Services"""

    def post(self, data):
        """Create a new user with hashed password and validation."""
        try:
            # Check if user exists
            existing_user = (
                db.session.query(User)
                .filter(
                    (User.username == data["username"]) | (User.email == data["email"])
                )
                .first()
            )
            if existing_user:
                raise IntegrityError("Username or email already exists.", orig=None)

            # Create new user
            user = User(
                first_name=data["first_name"],
                last_name=data["last_name"],
                username=data["username"],
                email=data["email"],
            )

            # Hash password
            user.set_password(data["password"])

            db.session.add(user)
            db.session.commit()

            return user.to_dict()

        except IntegrityError:
            db.session.rollback()
            return success_response(
                status_code=409,
                message="Email address or username already in use.",
            )

        except Exception as e:
            db.session.rollback()
            return success_response(
                status_code=500,
                message="Internal server error.",
                data={"error": str(e)},
            )

    # fetch user by ID
    def get(self, user_id):
        """Fetch by ID"""
        user = check_model_existence(User, user_id)
        return success_response(
            status_code=200, message="User retrieved Successfully", data=user.to_dict()
        )

    # Update User
    def put(self, user_id, **kwargs):
        """Fully update user info"""
        user = check_model_existence(User, user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return user.to_dict()

    # delete User
    def delete(self, user_id):
        """soft delete a User"""
        user = check_model_existence(User, user_id)
        if user.is_deleted:
            raise ValueError("User is already deleted.")

        user.is_deleted = True
        db.session.commit()

        return user.to_dict()

    def set_last_login(self, user_id):
        """update the last login timestamp for users"""
        user = check_model_existence(User, user_id)
        user.last_login = datetime.utcnow()
        db.session.commit()

    def generate_jwt_token(self, user):
        """Generate JWT token for authenticated user"""
        try:
            token = create_access_token(
                identity=user.id,
                additional_claims={"email": user.email},
                expires_delta=timedelta(hours=1),
            )

            return token
        except Exception as e:
            db.session.rollback()
            return success_response(
                status_code=500,
                message="Internal server error.",
                data={"error": str(e)},
            )

    @staticmethod
    def get_user_by_email(email):
        """retrieve user by email"""
        try:
            return User.query.filter_by(email=email).first()
        except Exception as e:
            db.session.rollback()
            return success_response(
                status_code=500,
                message="Internal server error.",
                data={"error": str(e)},
            )

    def authenticate(self, email, password):
        """Authenticate a user by username and password"""
        try:
            user = User.query.filter_by(email=email).first()

            if not user or not user.check_password(password):
                raise ValueError("Invalid email or password")

            # Generate JWT token
            token = self.generate_jwt_token(user)

            # add user data and token to response
            user_data = user.to_dict()
            user_data["token"] = token

            return user_data

        except IntegrityError:
            db.session.rollback()
            return success_response(
                status_code=401,
                message="Invalid email or password",
            )

        except Exception as e:
            db.session.rollback()
            return success_response(
                status_code=500,
                message="Internal server error.",
                data={"error": str(e)},
            )

    def generate_reset_link(self, user):
        """
        Generates a password reset link for the user.
        """
        secret_key = current_app.config.get("SECRET_KEY")
        salt = current_app.config.get("SALT")
        try:
            serializer = URLSafeTimedSerializer(secret_key)
            token = serializer.dumps({"id": user.id}, salt=salt)

            # Construct the reset
            base_url = current_app.config.get("FRONTEND_URL", "http://127.0.0.1:7000")
            reset_link = f"{base_url}/api/v1/users/password-reset/verify?token={token}"
            return reset_link

        except Exception as e:
            db.session.rollback()
            return success_response(
                status_code=500,
                message="Internal server error.",
                data={"error": str(e)},
            )

    @staticmethod
    def get_user_by_reset_token(token):
        """get user by reset token"""
        secret_key = current_app.config.get("SECRET_KEY")
        salt = current_app.config.get("SALT")

        try:
            serializer = URLSafeTimedSerializer(secret_key)
            data = serializer.loads(token, salt=salt)
            user = User.query.get(data["id"])
            if not user:
                raise ValueError("User not found.")
            return user
        except Exception as e:
            return success_response(
                status_code=500, message="Internal Server Error", data={"error": str(e)}
            )

    @staticmethod
    def verify_reset_token(token, max_age=3600):
        """
        Verifies the reset token and returns the user's ID if valid.
        """
        secret_key = current_app.config.get("SECRET_KEY")
        salt = current_app.config.get("SALT")
        serializer = URLSafeTimedSerializer(secret_key)
        try:
            data = serializer.loads(token, salt=salt, max_age=max_age)
            return data["id"]
        except Exception as e:
            return success_response(
                status_code=500, message="Internal Server Error", data={"error": str(e)}
            )


user_service = UserService()
