from marshmallow import fields, validate
from application.schema import ma


class CustomerSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    phone = fields.String(required=True, validate=validate.Length(min=10))

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


class EmployeeSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True, validate=validate.Length(min=1))
    position = fields.String(required=True)

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

class OrderSchema(ma.Schema):
    id = fields.Integer()
    date = fields.Date(required=True)
    customer_id = fields.Integer(required=True)
    products = fields.Nested('ProductSchemaID', many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

class ProductSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True, validate=validate.Length(min=1))
    price = fields.Float(required=True, validate=validate.Range(min=0))

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

class ProductSchemaID(ma.Schema):
    id = fields.Integer(required=True)



class ProductionSchema(ma.Schema):
    id = fields.Integer()
    quantity = fields.Integer(required=True, validate=validate.Range(min=0))
    product_id = fields.Integer(required=True)
    date_produced = fields.Date(required=True)
    employees = fields.List(fields.Int(), required=True)

production_schema = ProductionSchema()
productions_schema = ProductionSchema(many=True)

class UserSchema(ma.Schema):
    id = fields.Integer()
    username = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=1))
    role = fields.String(required=True, validate=validate.Length(min=1))

user_schema = UserSchema()
users_schema = UserSchema(many=True)


