#!/usr/bin/env python3

# Import
from flask import jsonify, make_response
from typing import Optional


def success_response(status_code: int, message: str, data: Optional[dict] = None):
    """ Return a Json response for successful requests."""
    
    response_data = {
        "status_code": status_code,
        "success": status_code < 400,
        "message": message
    }
    
    if data is not None:
        response_data["data"] = data
        
    return make_response(jsonify(response_data), status_code)