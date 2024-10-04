from flask import jsonify
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash

from application.database import db
from models import User, Role
from circuitbreaker import circuit
from sqlalchemy import select, func
from utils.util import encode_token

def fallback_function(user):
    return None

@circuit(fallback_function=fallback_function)
def save(user_data):
    try:
        with Session(db.engine) as session:
            with session.begin():
                role = session.query(Role).filter_by(name=user_data['role']).first()
                if not role:
                    return None

                new_user = User(username=user_data['username'], role=role)
                new_user.hash_password(user_data['password'])
                session.add(new_user)
                session.commit()
            session.refresh(new_user)
            return new_user
    except Exception as e:
        raise e

def find_all():
    query = select(User)
    users = db.session.execute(query).scalars().all()
    return users


def login_user(username, password):
    user = db.session.query(User).filter_by(username=username).first()
    role_names = [role.role_name for role in user.roles]

    if user and check_password_hash(user.password, password):
        auth_token = encode_token(user.id, role_names)

        resp = {
            "status": "success",
            "message": "Successfully logged in.",
            "auth_token": auth_token
        }
        return resp

    return None