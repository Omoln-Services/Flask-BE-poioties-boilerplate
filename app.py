#!/usr/bin/python3

# imports
from flask import Flask
from flask_restx import Api
from api.utils.config import Config
from decouple import config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import logging
from api.db.database import db



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
    
    print("SQLAlchemy URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    
    # Initialize JWT Manager
    jwt = JWTManager(app)
    
    # Import and add Namespaces to the Api
    from api.v1.routes.users import user_ns
    api.add_namespace(user_ns, path='/api/v1/users')
    
    # Configure CORS to allow requests from any origin
    CORS(app, supports_credentials=True)

    @app.route("/")
    def hello_world():
        return "<p>Welcome to poiótēs Api 🎉{version 0.1.0}</p>"
    
        
    @app.route("/test_db")
    def test_db():
        # Test querying a simple model to confirm db connection
        return {"status": "database connected"} if db.engine else {"status": "no database connection"}        
    
    # Create the database tables
    with app.app_context():
        db.create_all()
        
    # Initialize additional apps
    api.init_app(app)

    # Return the Flask app instance
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=7000, debug=True)