from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from config import db
import re
from .cart_item import CartItem

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    serialize_rules = (
        '-user',
        '-cart_items',
        '-orders',
        '-reviews',
    )

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    mobile = db.Column(db.String)
    nickname = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='customer')
    cart_items = db.relationship('CartItem', back_populates='customer', cascade='all, delete-orphan')
    orders = db.relationship('Order', back_populates='customer', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')

    items_thru_cart = association_proxy('cart_items', 'item',
                        creator=lambda item_obj: CartItem(item=item_obj))
    
    @validates('first_name', 'last_name', 'mobile')
    def validate(self, key, value):
        if key == 'first_name' or key == 'last_name':
            if len(value) == 0:
                raise ValueError(f'Server validation error: No {"first name" if key == "first_name" else "last name"}')
        elif key == 'mobile':
            mobile = r"((([\(]?[0-9]{3,4}[\)]\s?)|([0-9]{3,4}[\-]))[0-9]{3,4}[\-][0-9]{4})|([0-9]{10,12})"
            mobile_regex = re.compile(mobile)
            if not mobile_regex.fullmatch(value):
                raise ValueError('Server validation error: Invalid mobile number')
            
        return value

    def __repr__(self):
        return f'<Customer {self.id}>'
