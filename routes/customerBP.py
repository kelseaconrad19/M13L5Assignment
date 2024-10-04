from flask import Blueprint
from controllers.customerController import save, find_all, customer_lifetime_value

customer_blueprint = Blueprint('customer_bp', __name__)

customer_blueprint.route('/', methods=['POST'])(save)
customer_blueprint.route('/', methods=['GET'])(find_all)
customer_blueprint.route('/customer_value', methods=['GET'])(customer_lifetime_value)