#!/usr/bin/env python3

# Import

from flask import request, session
from api.v1.services.users import user_service
from api.v1.models.users import User
from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required


user_ns = Namespace("users", description="user related operations")


# Define API model for input validation
register_model = user_ns.model(
    "register",
    {
        "first_name": fields.String(required=True, description="user firstname"),
        "last_name": fields.String(required=True, description="user lastname"),
        "email": fields.String(required=True, description="user email"),
        "password": fields.String(required=True, description="user password"),
        "username": fields.String(required=True, description="user username"),
    },
)


@user_ns.route("/register")
class CreateUser(Resource):
    """a class for users registration"""

    @user_ns.expect(register_model, validate=True)
    @user_ns.doc(description="Register a new user")
    @user_ns.response(201, "User registered successfully")
    @user_ns.response(409, "Email address or username already in use")
    @user_ns.response(400, "Missing required fields")
    @user_ns.response(500, "Internal server error")
    def post(self):
        """
        A function that handles users registration
        """
        data = request.get_json()

        # Initialize user registration with data validation within the service
        response = user_service.post(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            username=data.get("username"),
            password=data.get("password"),
            email=data.get("email"),
        )

        # Return the response generated from user_service
        return response


# Define the nested UserProfileData model
user_profile_data_model = user_ns.model(name='user profile', model={
    "id": fields.String(description="User ID"),
    "created_at": fields.DateTime(description="Account creation date"),
    "email": fields.String(description="User email address"),
    "avatar_url": fields.String(description="Avatar URL"),
    "is_active": fields.Boolean(description="Is the user active?"),
    "username": fields.String(description="Username"),
})


@user_ns.route("/me")
class GetUserProfile(Resource):
    """class to get user profile"""

    @user_ns.doc(description="Retrieve the authenticated user's profile")
    @user_ns.response(200, "User profile retrieved successfully", user_profile_data_model)
    @user_ns.response(401, "Authentication required")
    @user_ns.response(404, "User profile not found")
    @user_ns.response(500, "Internal server error")
    @jwt_required()
    def get(self):
        """function that gets user's profile information"""
        try:
            user_id = get_jwt_identity()
            if not user_id:
                response = {
                    "message": "Authentication required"
                }
                return response, 401

            user_profile = user_service.get(user_id=user_id)
            return user_profile
        except Exception as e:
            response = {
                "message": "Internal server error", "error": str(e)
            }
            return response, 500
