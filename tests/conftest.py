# conftest.py
import pytest
from app import create_app


@pytest.fixture(scope="session")
def client():
    """Create an instance of the Flask app."""
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        with app.test_client() as client:
            yield client
    if not app.config.get("SECRET_KEY"):
        raise ValueError("SECRET_KEY is not set in the .env")
