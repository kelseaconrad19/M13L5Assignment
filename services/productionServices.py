from flask import jsonify
from sqlalchemy.orm import Session, joinedload
from application.database import db
from models import Production, Employee, Product
from circuitbreaker import circuit
from sqlalchemy import select, func

def fallback_function(production):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(production_data):
    with Session(db.engine) as session:
        with session.begin():
            new_production = Production(product_id=production_data['id'], quantity=production_data['quantity'], date_produced=production_data['date_produced'])
            db.session.add(new_production)
            db.session.commit()
        session.close()
        return new_production

def find_all():
    session = db.session
    # Fetch all productions with their associated employees
    productions = session.query(Production).options(joinedload(Production.employees)).all()

    # Create a list to store the response
    production_response = []
    for production in productions:
        production_response.append({
            "id": production.id,
            "quantity": production.quantity,
            "product_id": production.product_id,
            "date_produced": production.date_produced.strftime('%Y-%m-%d'),
            "employees": [employee.id for employee in production.employees]  # Get employee IDs
        })

    # Return the JSON response
    return production_response
    # productions = []
    # for result in results:
    #     productions.append({
    #         "id": result.id,
    #         "quantity": result.quantity,
    #         "product_id": result.product_id,
    #         "date_produced": result.date_produced.strftime('%Y-%m-%d'),  # Ensure date is formatted correctly
    #         "employees": [employee.id for employee in result.employees]
    #     })
    #
    # # production_totals = [{"employee_name": row[0], "total_quantity": row[1]} for row in result]
    # return jsonify(productions)


def total_quantity_by_employee():
    result = find_all()
    return jsonify(result)


def evaluate_production_efficiency(date):
    session = db.session

    subquery = session.query(Production).filter(Production.date_produced == date).subquery()

    query = session.query(
        Product.name,
        func.sum(Production.quantity).label('total_quantity_produced')).join(Production, Production.product_id == Product.id).filter(Production.date_produced == date).group_by(Product.name)

    result = session.execute(query).all()

    production_efficiency = [{"product_name": row[0], "total_quantity_produced": row[1]} for row in result]

    return production_efficiency