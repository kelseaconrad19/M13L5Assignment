from flask import jsonify
from sqlalchemy.orm import Session
from application.database import db
from models import Customer, Order, Product, order_product
from circuitbreaker import circuit
from sqlalchemy import select, func

def fallback_function(customer):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(customer_data):
    try:
        if customer_data["name"] == "Failure":
            raise Exception("Failure condition triggered.")
        with Session(db.engine) as session:
            with session.begin():
                new_customer = Customer(name=customer_data["name"], email=customer_data["email"], phone=customer_data["phone"])
                session.add(new_customer)
                session.commit()
            session.refresh(new_customer)
            return new_customer
    except Exception as e:
        raise e

def find_all():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers


def find_customer_lifetime_value():
    session = db.session

    query = session.query(
        Customer.name,
        func.sum(Product.price * order_product.c.quantity).label('total_order_value')).join(Order, Customer.id == Order.customer_id).join(order_product, Order.id == order_product.c.order_id).join(Product, order_product.c.product_id == Product.id).group_by(Customer.name).having(func.sum(Product.price * order_product.c.quantity))

    result = session.execute(query).all()

    customer_lifetime_values = [{"customer_name": row[0], "total_order_value": row[1]} for row in result]

    return customer_lifetime_values

def customer_lifetime_value():
    result = find_customer_lifetime_value()
    return jsonify(result)