#!/usr/bin/env python3

# Import

from flask import request
from api.v1.services.users import user_service
from api.v1.models.users import User
from flask_restx import Namespace, Resource, fields, reqparse


user_ns = Namespace('users', description='user related operations')


# Define API model for input validation
register_model = user_ns.model('register', {
    'first_name': fields.String(required=True, description='user firstname'),
    'last_name': fields.String(required=True, description='user lastname'),
    'email': fields.String(required=True, description='user email'),
    'password': fields.String(required=True, description='user password'),
    'username': fields.String(required=True, description='user username'),
})

@user_ns.route('/register')
class CreateUser(Resource):
    """ a class for users registration """
    @user_ns.expect(register_model, validate=True)
    @user_ns.doc(description="Register a new user")
    @user_ns.response(201, 'User registered successfully')
    @user_ns.response(409, 'Email address or username already in use')
    @user_ns.response(400, 'Missing required fields')
    @user_ns.response(500, 'Internal server error')
        
    def post(self):
        """
        A function that handles users registration
        """
        data = request.get_json()

        # Initialize user registration with data validation within the service
        response = user_service.post(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            username=data.get('username'),
            password=data.get('password'),
            email=data.get('email')
        )

        # Return the response generated from user_service
        return response

