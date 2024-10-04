from sqlalchemy import select
from application.database import db
from models import Order, Product, Customer
from circuitbreaker import circuit

def fallback_function(order):
    return None
@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(order_data):
    session = db.session
    product_ids = [product['id'] for product in order_data['products']]
    products = session.query(Product).filter(Product.id.in_(product_ids)).all()

    customer_id = order_data['customer_id']
    customer = session.query(Customer).get(customer_id)

    if len(products) != len(product_ids):
        raise ValueError('One or more products not found')
    if not customer:
        raise ValueError(f'Customer with ID {customer_id} not found')

    print("Products:", products[0].name)
    new_order = Order(customer_id=order_data['customer_id'])
    new_order.products.extend(products)
    try:
        session.add(new_order)
        session.commit()
    except Exception as e:
        session.rollback()
        raise

    session.refresh(new_order)
    for product in new_order.products:
        session.refresh(product)

    return new_order

def find_all():
    session = db.session
    query = select(Order)
    orders = session.execute(query).scalars().all()
    return orders

def find_all_pagination(page=1, per_page=10):
    orders = db.paginate(select(Order), page=page, per_page=per_page)
    return orders

