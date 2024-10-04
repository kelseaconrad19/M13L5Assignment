from application.database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from typing import List
from werkzeug.security import generate_password_hash, check_password_hash

order_product = db.Table(
    'Order_Product',
    Base.metadata,
    db.Column('order_id', db.ForeignKey('Orders.id')),
    db.Column('product_id', db.ForeignKey('Products.id')),
    db.Column('quantity', db.Integer, nullable=False)
)

class Customer(Base):
    __tablename__ = "Customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(320))
    phone: Mapped[str] = mapped_column(db.String(15))
    orders: Mapped[list["Order"]] = db.relationship(back_populates='customer')

class Employee(Base):
    __tablename__ = 'Employees'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    position: Mapped[str] = mapped_column(db.String(320))
    production_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('Production.id'), nullable=True)
    production: Mapped["Production"] = db.relationship("Production", back_populates='employees')

class Order(Base):
    __tablename__ = 'Orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    # date: Mapped[datetime.date] = mapped_column(db.Date, nullable=False)
    customer_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('Customers.id'))
    customer: Mapped["Customer"] = db.relationship(back_populates="orders")
    products: Mapped[List["Product"]] = db.relationship(secondary=order_product)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)

class Product(Base):
    __tablename__ = 'Products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

class Production(Base):
    __tablename__ = 'Production'
    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)
    product_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('Products.id'))
    date_produced: Mapped[datetime.date] = mapped_column(db.Date, nullable=False)
    employees: Mapped[List["Employee"]] = db.relationship("Employee", back_populates="production")

class User(Base):
    __tablename__ = 'Users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    role_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('Roles.id'), nullable=False)
    role: Mapped["Role"] = db.relationship("Role", back_populates="users")

    def hash_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}, Role: {self.role}>'

class Role(Base):
    __tablename__ = 'Roles'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50), unique=True, nullable=False)
    users: Mapped[list["User"]] = db.relationship("User", back_populates="role")
