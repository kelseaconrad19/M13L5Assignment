import flask
from flask import request, jsonify
from schemas import product_schema, products_schema
import services.productServices as productService
from marshmallow import ValidationError


def save():
    try:
        product_data = product_schema.load(flask.request.json)

    except ValidationError as err:
        return flask.jsonify(err.messages), 400

    product_save = productService.save(product_data)
    if product_save is not None:
        return product_schema.jsonify(product_save), 201
    else:
        return flask.jsonify({'message': 'Fallback method error activated', 'body': product_data}), 400

def find_all():
    products = productService.find_all()
    return products_schema.jsonify(products), 200

def find_all_pagination():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return products_schema.jsonify(productService.find_all_pagination(page, per_page)), 200

def top_selling_products():
    return productService.top_selling_products(), 200