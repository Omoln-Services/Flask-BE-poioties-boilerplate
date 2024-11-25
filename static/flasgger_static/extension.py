# extensions.py
from flask_restx import Api
from flask import Blueprint, render_template

# Initialize the Api object
# Create the API instance
api = Api(
    version="1.0",
    title="Poioties API",
    description="Poioties Flask API with Flask-RESTX",
    doc="/",
)

# Create a Blueprint for the custom Swagger UI
swagger_blueprint = Blueprint("swagger", __name__, template_folder="templates")


@swagger_blueprint.route("")
def swagger_ui():
    return render_template("swagger.html")


def init_app(app):
    api.init_app(app)
