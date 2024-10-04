from flask import jsonify
from sqlalchemy.orm import Session
from application.database import db
from models import Product, Order, order_product
from circuitbreaker import circuit
from sqlalchemy import select, func

from services import productionServices


def fallback_function(product):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(product_data):
    if product_data["name"] == "Failure":
        raise Exception("Failure")
    with Session(db.engine) as session:
        with session.begin():
            new_product = Product(name=product_data["name"], price=product_data["price"])
            db.session.add(new_product)
            db.session.commit()
        db.session.refresh(new_product)
        return new_product

def find_all():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    return products

def find_top_selling_products():
    session = db.session

    query = select(
        Product.name,
        func.sum(order_product.c.quantity).label('total_quantity_ordered')).join(order_product, Product.id == order_product.c.product_id).group_by(Product.name).order_by(func.sum(order_product.c.quantity).desc())

    result = session.execute(query).all()

    top_selling_products = [{"product_name": row[0], "total_quantity_ordered": row[1]} for row in result]

    return top_selling_products

def find_all_pagination(page=1, per_page=10):
    products = db.paginate(select(Product), page=page, per_page=per_page)
    return products

def top_selling_products():
    result = find_top_selling_products()
    return jsonify(result)

