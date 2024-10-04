from flask import request, jsonify

from schemas import production_schema, productions_schema
import services.productionServices as productionService
from marshmallow import ValidationError

def save():
    try:
        production_data = production_schema.load(request.get_json())

    except ValidationError as err:
        return jsonify(err.messages), 422

    production_save = productionService.save(production_data)
    if production_save is not None:
        return production_schema.jsonify(production_save), 201
    else:
        return jsonify({'message': 'Fallback method error activated', 'body': production_data}), 400

# @create_cache().cached(timeout=60)
def find_all():
    productions = productionService.find_all()
    return productions_schema.jsonify(productions), 200

def production_efficiency():
    production_date = "2024-09-15"
    result = productionService.evaluate_production_efficiency(production_date)
    return jsonify(result)