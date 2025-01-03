from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from config import db, bcrypt
import re

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = (
        '-_password_hash',
        '-seller.user',
        '-seller.items.category',
        '-seller.items.seller',
        '-seller.items.cart_items',
        '-seller.items.order_items.order.customer.user',
        '-seller.items.order_items.order.customer.cart_items',
        '-seller.items.order_items.order.customer.orders',
        '-seller.items.order_items.order.customer.reviews',
        '-seller.items.order_items.order.order_items',
        '-seller.items.order_items.item',
        '-seller.items.reviews',
        '-customer.user',
        '-customer.cart_items.item.category',
        '-customer.cart_items.item.seller',
        '-customer.cart_items.item.cart_items',
        '-customer.cart_items.item.order_items',
        '-customer.cart_items.item.reviews',
        '-customer.cart_items.customer',
        '-customer.orders.customer',
        '-customer.orders.order_items.order',
        '-customer.orders.order_items.item.category',
        '-customer.orders.order_items.item.seller',
        '-customer.orders.order_items.item.cart_items',
        '-customer.orders.order_items.item.order_items',
        '-customer.orders.order_items.item.reviews',
        '-customer.reviews.item.category',
        '-customer.reviews.item.seller',
        '-customer.reviews.item.cart_items',
        '-customer.reviews.item.order_items',
        '-customer.reviews.item.reviews',
        '-customer.reviews.customer',
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    phone = db.Column(db.String)    
    street_1 = db.Column(db.String)
    street_2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.String)

    seller = db.relationship('Seller', back_populates='user', uselist=False)
    customer = db.relationship('Customer', back_populates='user', uselist=False)

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    @validates('username', 'password', 'email', 'phone', 'zip_code')
    def validate(self, key, value):
        if key == 'username':
            if not isinstance(value, str):
                raise TypeError('Server validation error: Invalid type for username')
            elif len(value) < 5 or len(value) > 20:
                raise ValueError('Server validation error: Invalid username')
        elif key == 'password':
            if len(value) < 5:
                raise ValueError('Server validation error: Invalid password length')
        elif key == 'email':
            email = r"[A-Za-z]+[A-Za-z0-9]*\.?[A-Za-z0-9]+@[A-Za-z_\-]+\.[A-Za-z]{2,3}"
            email_regex = re.compile(email)
            if not email_regex.fullmatch(value):
                raise ValueError('Server validation error: Invalid email address')
        elif key == 'phone':
            phone = r"((([\(]?[0-9]{3,4}[\)]\s?)|([0-9]{3,4}[\-]))[0-9]{3,4}[\-][0-9]{4})|([0-9]{10,12})"
            phone_regex = re.compile(phone)
            if not phone_regex.fullmatch(value):
                raise ValueError('Server validation error: Invalid phone number')
        elif key == 'zip_code':
            zip_code = r"[0-9]{5}"
            zip_code_regex = re.compile(zip_code)
            if not zip_code_regex.fullmatch(value):
                raise ValueError('Server validation error: Invalid zip code')

        return value

    def __repr__(self):
        return f'<User {self.id}>'

