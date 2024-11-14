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
    
    # Database URI based on DB_TYPE environment variable
    DB_TYPE = os.getenv('DB_TYPE')
        
    if DB_TYPE == 'postgresql':
        SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    elif DB_TYPE == 'mysql':
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    else:
        raise ValueError("Unsupported DB_TYPE. Use 'postgresql' or 'mysql'")
                
    # Disable track modifictions to avoid warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configureation clas
    """
    DEGUB = True


class TestingConfig(Config):
    """Testing configuration class
    """
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration class"""

    DEBUG = False


# Mapping config names to their respective classes
config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

# Set the active configuration based on an environment variable
active_env = os.getenv("FLASK_ENV", "development")
config = config_map[active_env]
