import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify

import jwt
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

def encode_token(user_id, role_names):
    try:
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(hours=1),
            'iat': datetime.now(timezone.utc),
            'sub': user_id,
            'roles': role_names
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token
    except Exception as e:
        return str(e)

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(' ')[1]
            if not token:
                return jsonify({'message': 'Authentication token is missing', 'error': 'Unauthorized'}), 401

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired', 'error': 'Unauthorized'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token', 'error': 'Unauthorized'}), 401

            roles = payload['roles']

            if role not in roles:
                return jsonify({'message': 'User does not have the required role', 'error': 'Forbidden'}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator