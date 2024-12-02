from flask import abort
from api.db.database import db


def check_model_existence(model, id):
    """Check if a model exists by its ID"""
    obj = db.session.get(model, id)

    if not obj:
        abort(404, description=f"{model.__name__} does not exist")

    return obj


def get_model_or_none(model, id):
    """this function returns the obj
    if it exists and `None`
    """
    return db.session.get(model, id)
