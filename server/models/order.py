from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import db
import re

class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    serialize_rules = (
        '-customer',
        '-order_items.order',
        '-order_items.item',
    )

    id = db.Column(db.Integer, primary_key=True)
    ordered_date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    closed_date = db.Column(db.DateTime)
    street_1 = db.Column(db.String)
    street_2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    # relationship
    customer = db.relationship('Customer', back_populates='orders')
    order_items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')

    @validates('zip_code')
    def validate(self, key, value):
        if key == 'zip_code':
            zip_code = r"[0-9]{5}"
            zip_code_regex = re.compile(zip_code)
            if not zip_code_regex.fullmatch(value):
                raise ValueError('Server validation error: Invalid zip code')

        return value
            

    def __repr__(self):
        return f'<Order {self.id}>'