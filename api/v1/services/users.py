#!/usr/bin/env python3

# Import
from flask import abort
from api.utils.db_validator import check_model_existence
from api.utils.success_response import success_response
from sqlalchemy.exc import IntegrityError
from api.core.base.services import Service
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
import os
from api.v1.models.users import User
from api.db.database import db


class UserService(Service):
    """User Services"""

    def post(self, first_name, last_name, username, password, email):
        """Create a new user with hashed password and validation."""
        required_fields = [first_name, last_name, username, password, email]
        if not all(required_fields):
            return success_response(
                status_code=400,
                message="Missing required fields",
                data={
                    "errors": [
                        field
                        for field in [
                            "first_name",
                            "last_name",
                            "username",
                            "password",
                            "email",
                        ]
                        if not locals().get(field)
                    ]
                },
            )

        try:
            existing_user = (
                db.session.query(User)
                .filter((User.username == username) | (User.email == email))
                .first()
            )

            if existing_user:
                return success_response(
                    status_code=409,
                    message="A user with this username or email already exists.",
                )

            user = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
            )
            # Hashes and sets password
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            return success_response(
                status_code=201,
                message="User registered successfully",
                data=user.to_dict(),
            )

        except IntegrityError:
            db.session.rollback()
            return success_response(
                status_code=409,
                message="Email address or username already in use.",
            )

        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
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

    # Update User by ID
    def update(self, user_id, **kwargs):
        """update user info"""
        user = check_model_existence(User, user_id)

        # update only the provided fields
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        db.session.commit()
        return success_response(
            status_code=200, message="User updated Successfully", data=user.to_dict()
        )

    def put(self, user_id, **kwargs):
        """Fully update user info"""
        user = check_model_existence(User, user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return success_response(
            status_code=200,
            message="User fully updated Successfully",
            data=user.to_dict(),
        )

    # delete User
    def delete(self, user_id):
        """soft delete a User"""
        user = check_model_existence(User, user_id)
        user.is_deleted = True
        db.session.commit()

        return success_response(200, "user deleted Successfully", data=user.to_dict())

    def set_last_login(self, user_id):
        """update the last login timestamp for users"""
        user = check_model_existence(User, user_id)
        user.last_login = datetime.utcnow()
        db.session.commit()

    def generate_jwt_token(self, user):
        """Generate JWT token for authenticated user"""
        token = create_access_token(
            identity=user.id,
            additional_claims={"username": user.username},
            expires_delta=timedelta(hours=1),
        )

        return token

    def authenticate(self, username, password):
        """Authenticate a user by username and password"""
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # Generate JWT token
            token = self.generate_jwt_token(user)

            # add user data and token to response
            user_data = user.to_dict()
            user_data["token"] = token

            return success_response(
                status_code=200,
                message="User authenticated successfully",
                data=user_data,
            )

        abort(401, description="Invalid username or password")


user_service = UserService()
