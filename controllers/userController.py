from flask import request, jsonify

from application.database import db
from models import User
from schemas import user_schema, users_schema
import services.userService as userService
from marshmallow import ValidationError

from utils.util import encode_token, decode_token, role_required


def save():
    try:
        user_data = user_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400

    user_save = userService.save(user_data)
    if user_save is not None:
        return user_schema.jsonify(user_save), 201
    else:
        return jsonify({"message": "Fallback method error activated", "body": user_data}), 400

@role_required('admin')
def find_all():
    users = userService.find_all()
    return users_schema.jsonify(users), 200

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = db.session.query(User).filter_by(username=username).first()

    if user and user.verify_password(password):
        # Generate a JWT token
        auth_token = encode_token(user.id, user.role.name)
        return jsonify({'token': auth_token}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

def verify_token():
    token = request.headers.get('Authorization')
    if token:
        user_id = decode_token(token)
        if isinstance(user_id, int):
            return jsonify({"user_id": user_id})
        else:
            return jsonify({"error": user_id}), 401
    else:
        return jsonify({"error": "Token is missing"}), 400




