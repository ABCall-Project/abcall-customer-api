from functools import wraps
from http import HTTPStatus
from flask import request

def validate_customer():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            name = request.form.get('name')

            if not name or name == "":
                return {"message": "Name cannot be empty"}, HTTPStatus.BAD_REQUEST

            if len(name) > 100:
                return {"message": "The Name is not complete with the maximum, should be 100 characters"}, HTTPStatus.BAD_REQUEST

            return f(*args, **kwargs)
        return decorated_function
    return decorator