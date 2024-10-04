from flask import request, jsonify
from schemas import order_schema, orders_schema, customers_schema
import services.orderServices as orderServices
from marshmallow import ValidationError

def save():
    try:
        order_data = order_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400

    order_save = orderServices.save(order_data)
    if order_save is not None:
        return order_schema.jsonify(order_save), 201
    else:
        return jsonify({'message': 'Fallback method error activated', 'body': order_data}), 400

def find_all():
    orders = orderServices.find_all()
    return orders_schema.jsonify(orders), 200

def find_all_pagination():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return orders_schema.jsonify(orderServices.find_all_pagination(page, per_page)), 200
