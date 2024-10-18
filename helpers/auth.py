# helpers/auth.py
from functools import wraps
from flask import request, jsonify
import os

# Load the API key from the environment variable
API_KEY = os.getenv('API_KEY')

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if api_key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function
