#!/usr/bin/env python3

# Import
import logging
from flask import request
from flask_restx import Resource, fields
from api.utils.success_response import success_response
from api.v1.services.users import user_service
from . import user_ns

logging.basicConfig(level=logging.DEBUG)


login_model = user_ns.model(
    "login",
    {
        "email": fields.String(required=True, description="user email"),
        "password": fields.String(required=True, description="user password"),
    },
)


@user_ns.route("/login")
class Login(Resource):
    """user login docs with flask restx"""

    @user_ns.expect(login_model, validate=True)
    @user_ns.doc(description="Api that handles user login credentials")
    @user_ns.response(200, "User authenticated successfully")
    @user_ns.response(401, "Invalid email or password")
    @user_ns.response(400, "Email and password are required")
    @user_ns.response(500, "Social login failed. Try again.")
    def post(self):
        """A route that handle's user login credentials"""

        data = request.get_json()

        # Check if email and password are provided
        if not data.get("email") or not data.get("password"):
            return success_response(
                status_code=400,
                message="Email and password are required",
                data={"error": "Missing email or password"},
            )

        response = user_service.authenticate(
            email=data.get("email"), password=data.get("password")
        )

        if response.get("status_code") in [401, 500]:
            return success_response(
                status_code=response["status_code"],
                message=response["message"],
                data=response,
            )

        return success_response(
            status_code=200,
            message="User authenticated successfully",
            data=response,
        )
