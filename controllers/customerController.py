from flask import request, jsonify

from schemas import customer_schema, customers_schema
import services.customerServices as customerService
from marshmallow import ValidationError

def save():
    #! Post request. /customers POST contain JSON
    try:
        #? Validate and deserialize input
        customer_data = customer_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400

    customer_save = customerService.save(customer_data)
    if customer_save is not None:
        return customer_schema.jsonify(customer_save), 201
    else:
        return jsonify({'message': 'Fallback method error activated', 'body': customer_data}), 400

def find_all():
    customers = customerService.find_all()
    return customers_schema.jsonify(customers), 200

def customer_lifetime_value():
    return customerService.customer_lifetime_value(), 200