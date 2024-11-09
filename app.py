#!/usr/bin/python3

# imports
from flask import Flask
from flask_restx import Api
from config import Config
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_jwt_extended import JWTManager
from flask_cors import CORS


# Initialize extensions
db = SQLAlchemy()
# Create the API instance
api = Api(
    version="1.0",
    title="Poioties API",
    description="Poioties Flask API with Flask-RESTX",
    doc='/docs'
)


def create_app():
    """
    Initializes the Flask app instance and all its dependencies
    """
    app = Flask(__name__)

    # Load configurations
    app.config.from_object(Config)

    # Initialize the database with the app context
    db.init_app(app)

    # Set the secret key from the .env file using python-decouple
    app.secret_key = config("SECRET_KEY")

    # Initialize JWT Manager
    jwt = JWTManager(app)

    @app.route("/")
    def hello_world():
        return "<h1>Welcome to Poioties Api {version 0.1.0}</h1>"

    # Configure CORS to allow requests from any origin
    CORS(app, supports_credentials=True)

    # Initialize additional apps/extensions if needed
    api.init_app(app)
    
    # Create the database tables
    with app.app_context():
        db.create_all()

    # Return the Flask app instance
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=7000, debug=True)
