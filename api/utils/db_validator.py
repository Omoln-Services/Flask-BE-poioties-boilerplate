from flask import abort


def check_model_existence(model, id):
    """Check if a model exists by its ID
    """
    obj = model.query.get(id)
    
    if not obj:
        abort(404, description=f"{model.__name__} does not exist")
    
    return obj


def get_model_or_none(model, id):
    """this function returns the obj
    if it exists and `None`
    """
    return model.query.get(id)