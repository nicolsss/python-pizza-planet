from functools import wraps
from flask import jsonify


def base_service(controller):
    @wraps(controller)
    def wrapper(*args, **kwargs):
        result, error = controller(*args, **kwargs)
        response = result if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code
    return wrapper
