from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from config import db
import json
from .cart_item import CartItem

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    serialize_rules = (
        '-category',
        '-seller',
        '-cart_items',
        '-order_items',
        '-reviews',
    )

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Integer, default=1)
    name = db.Column(db.String, nullable=False)
    brand = db.Column(db.String)
    default_item_idx = db.Column(db.Integer, nullable=False)
    prices = db.Column(db.String)   # list: price by package type
    discount_prices = db.Column(db.String)  # list: discount price by package type
    amounts = db.Column(db.String)    # list: amount by package type
    units = db.Column(db.String)    # list: unit by package type
    packs = db.Column(db.String)    # list: package type
    about_item = db.Column(db.String)   # object: item characteristics
    details_1 = db.Column(db.String)    # object: item details
    details_2 = db.Column(db.String)    # object: item details
    images = db.Column(db.String)   # list:
    accum_sales_cnt = db.Column(db.Integer, default=0)
    avg_review_rating = db.Column(db.Float, default=0)
    accum_review_cnt = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))    # Removal Candidate
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'))

    category = db.relationship('Category', back_populates='items')
    seller = db.relationship('Seller', back_populates='items')
    cart_items = db.relationship('CartItem', back_populates='item', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', back_populates='item', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='item', cascade='all, delete-orphan')

    customers_thru_cart = association_proxy('cart_items', 'customer',
                            creator=lambda customer_obj : CartItem(customer=customer_obj))
    

    def validate_list(self, key, value, allowed_types):
        if not isinstance(value, list):
            raise TypeError(f'{key} must be a list.')
        elif len(value) == 0: 
            raise ValueError(f'{key} must be a non-empty list.')
        else: 
            for val in value:
                valid_type = False
                for type in allowed_types:
                    valid_type = valid_type or isinstance(val, type)
                if not valid_type:
                    raise ValueError(f'{key} must be a list of {allowed_types}.')

    @validates('name', 'prices', 'discount_prices', 'amounts', 'packs', 'units', 
        'about_item', 'details_1', 'details_2', 'images')
    def validate(self, key, value):
        if key == 'name':
            if len(value) == 0:
                raise ValueError('Name is required')
            elif len(value) > 200:
                raise ValueError("Name can't exceed more than 200 characters")
        elif key == 'prices' or key == 'discount_prices' or key == 'amounts':
            self.validate_list(key, value, [int, float])
            return json.dumps(value)
        elif key == 'packs':
            self.validate_list(key, value, [int])
            return json.dumps(value)
        elif key == 'units' or key == 'about_item':
            self.validate_list(key, value, [str])
            return json.dumps(value)
        elif key == 'details_1' or key == 'details_2': 
            self.validate_list(key, value, [str])
            for val in value:
                slist = val.split(';-;')
                if len(slist) != 2 or len(slist[0]) == 0 or len(slist[1]) == 0:
                    raise ValueError(f'{key} must be a list of key/value pair seperated by ";-;".')
            return json.dumps(value)
        elif key == 'images':
            self.validate_list(key, value, [str])
            if len(value) == 0 or len(value) > 10:
                raise ValueError(f'{key} must be a list of image links upto 10.')
            return json.dumps(value)

        return value
    
    def __repr__(self):
        return f'<Item {self.id}>'