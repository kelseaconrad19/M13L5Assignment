from typing import final

from flask import Flask, jsonify, app
from flask_sqlalchemy.session import Session
from werkzeug.security import generate_password_hash

from application.schema import ma
from application.database import db
from models import *
import datetime

from routes.customerBP import customer_blueprint
from routes.employeeBP import employee_blueprint
from routes.orderBP import order_blueprint
from routes.productBP import product_blueprint
from routes.productionBP import production_blueprint
from routes.userBP import user_blueprint
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "E Commerce API"
    }
)

def create_app(config_name):
    app = Flask(__name__, static_folder="../static")
    app.config.from_object(f'config.{config_name}')
    app.debug = True

    db.init_app(app)
    ma.init_app(app)

    return app


def init_info_data():
    session = db.session

    session.query(User).delete()
    session.commit()

    try:
        products = [
            Product(name="Shirt", price=12.99),
            Product(name="Pants", price=35.99),
            Product(name="Socks", price=9.99)
        ]
        session.add_all(products)
        session.commit()

        customers = [
            Customer(name="John Doe", email="john@example.com", phone="1231231234"),
            Customer(name="Jane Smith", email="jane@example.com", phone="9876543210")
        ]
        session.add_all(customers)
        session.commit()

        orders = [
            Order(customer_id=customers[0].id, quantity=5),
            Order(customer_id=customers[1].id, quantity=3)
        ]
        session.add_all(orders)
        session.commit()

        session.execute(order_product.insert().values(order_id=orders[0].id, product_id=products[0].id, quantity=2))
        session.execute(order_product.insert().values(order_id=orders[0].id, product_id=products[1].id, quantity=3))

        session.execute(order_product.insert().values(order_id=orders[1].id, product_id=products[1].id, quantity=1))
        session.execute(order_product.insert().values(order_id=orders[1].id, product_id=products[2].id, quantity=2))

        productions = [
            Production(quantity=100, product_id=products[0].id, date_produced=datetime.date(2024, 9, 15)),
            Production(quantity=200, product_id=products[1].id, date_produced=datetime.date(2024, 9, 16)),
            Production(quantity=300, product_id=products[2].id, date_produced=datetime.date(2024, 9, 17))
        ]
        session.add_all(productions)
        session.commit()

        employees = [
            Employee(name="Alice Johnson", position="Manager", production_id=1),
            Employee(name="Bob Williams", position="Worker", production_id=2)
        ]
        session.add_all(employees)
        session.commit()

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def blueprint_config(app):
    app.register_blueprint(customer_blueprint, url_prefix="/customers")
    app.register_blueprint(employee_blueprint, url_prefix="/employees")
    app.register_blueprint(order_blueprint, url_prefix="/orders")
    app.register_blueprint(product_blueprint, url_prefix="/products")
    app.register_blueprint(production_blueprint, url_prefix="/production")
    app.register_blueprint(user_blueprint, url_prefix="/users")
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def init_roles_data():
    with db.session.begin():
        roles = [
            Role(name='admin'),
            Role(name='user'),
            Role(name='guest')
        ]
        db.session.add_all(roles)

def init_users_data():
    with db.session.begin():

        user1 = User(username='user1', role_id=1)
        user1.hash_password('password1')

        user2 = User(username='user2', role_id=2)
        user2.hash_password('password2')

        user3 = User(username='user3', role_id=3)
        user3.hash_password('password3')

        db.session.add_all([user1, user2, user3])
    db.session.commit()

my_app = create_app('DevelopmentConfig')

if __name__ == "__main__":
    app = create_app('DevelopmentConfig')
    blueprint_config(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
        init_info_data()
        init_roles_data()
        init_users_data()

    app.run(debug=True)