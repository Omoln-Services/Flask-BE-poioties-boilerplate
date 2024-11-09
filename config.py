#!/usr/bin/python3

# imports
import os
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()


class Config():
    """
    base class configuration settings for database
    """

    SQLALCHEMY_DATABASE_URI = f"postgresql://{
        os.getenv('DB_USER')}:{
        os.getenv('DB_PASSWORD')}@{
            os.getenv('DB_HOST')}/{
                os.getenv('DB_NAME')}"
                
    # Disable track modifictions to avoid warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configureation clas
    """
    DEGUB = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL')


class TestingConfig(Config):
    """Testing configuration class
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL')
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration class"""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL')


# Mapping config names to their respective classes
config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

# Set the active configuration based on an environment variable
active_env = os.getenv("FLASK_ENV", "testing")
config = config_map[active_env]
